from energysim.database.exu_energy import ExecutionUnitEnergyDatabase
from energysim.execution.exu_metrics import ExecutionUnitMetrics


def execute_unit(node: str,
                 core_clock_in_ghz: float,
                 word_size_in_bytes: int,
                 agus: int,
                 agu_ops: int,
                 alus: int,
                 alu_ops: int,
                 fpus: int,
                 fpu_ops: int,
                 sfus: int,
                 sfu_ops: int,
                 total_critical_path_ops: int) -> 'ExecutionUnitMetrics':
    db = ExecutionUnitEnergyDatabase()
    full = db.load_data('../../data/exu_energy.csv')
    energies = db.lookupEnergySet(node, word_size_in_bytes)
    print(energies)
    exu_metrics = ExecutionUnitMetrics("execution_unit")
    exu_metrics.core_clock_ghz = core_clock_in_ghz
    exu_metrics.word_size = word_size_in_bytes
    exu_metrics.agus = agus
    exu_metrics.alus = alus
    exu_metrics.fpus = fpus
    exu_metrics.sfus = sfus

    ############################################################################
    # record the workload activity
    aggregate_agu_ops = agu_ops * agus
    aggregate_alu_ops = alu_ops * alus
    aggregate_fpu_ops = fpu_ops * fpus
    aggregate_sfu_ops = sfu_ops * sfus
    exu_metrics.record('agu', aggregate_agu_ops, energies.agu)
    exu_metrics.record('alu', aggregate_alu_ops, energies.alu)
    exu_metrics.record('fpu', aggregate_fpu_ops, energies.fpu)
    exu_metrics.record('sfu', aggregate_sfu_ops, energies.sfu)
    # we need to read two inputs for each operator, assume these are coming from the register file
    # to read from a register in the register file, we needed to write it
    # basic operation is
    # load, load, execute, writeback, store
    # both loads write into the register file, as does the writeback
    # the execute and store both read from the register file
    # so for every operator, we have 3 register writes and 3 register writes
    alu_reg_read = aggregate_alu_ops * 3
    alu_reg_write = aggregate_alu_ops * 3
    fpu_reg_read = aggregate_fpu_ops * 3
    fpu_reg_write = aggregate_fpu_ops * 3
    sfu_reg_read = aggregate_sfu_ops * 3
    sfu_reg_write = aggregate_sfu_ops * 3
    # AGU is slightly different, they tend to have one read and one write on the register file
    agu_reg_read = aggregate_agu_ops
    agu_reg_write = aggregate_agu_ops
    reg_read = agu_reg_read + alu_reg_read + fpu_reg_read + sfu_reg_read
    reg_write = agu_reg_write + alu_reg_write + fpu_reg_write + sfu_reg_write
    exu_metrics.record('reg_read', reg_read, energies.reg_read)
    exu_metrics.record('reg_write', reg_write, energies.reg_write)

    # consolidate sets
    exu_metrics.consolidate('compute', ['agu', 'alu', 'fpu', 'sfu'])
    exu_metrics.consolidate('data', ['reg_read', 'reg_write'])
    exu_metrics.consolidate('total', ['compute', 'data'])

    ############################################################################
    # calculate performance metrics

    # instruction throughput
    total_aops = exu_metrics.events['agu']  # address operations
    total_iops = exu_metrics.events['alu']  # ALU operations
    total_flops = exu_metrics.events['fpu'] # FPU operations
    total_sfops = exu_metrics.events['sfu'] # SFU operations
    total_ops = total_aops + total_iops + total_flops + total_sfops
    exu_metrics.total_aops = total_aops
    exu_metrics.total_iops = total_iops
    exu_metrics.total_flops = total_flops
    exu_metrics.total_sfops = total_sfops
    exu_metrics.total_ops = total_ops
    clock_cycle_ns = 1.0 / core_clock_in_ghz
    # total_critical_path_ops designates the number of operations that
    # sequentially measure the elapsed time
    total_elapsed_time_in_sec = total_critical_path_ops * clock_cycle_ns * 1.0e-9
    exu_metrics.elapsed_time = total_elapsed_time_in_sec

    ops_per_sec = total_ops / total_elapsed_time_in_sec
    iops_per_sec = total_iops / total_elapsed_time_in_sec
    flops_per_sec = total_flops / total_elapsed_time_in_sec
    sfops_per_sec = total_sfops / total_elapsed_time_in_sec
    exu_metrics.ops_per_sec = ops_per_sec
    exu_metrics.iops_per_sec = iops_per_sec
    exu_metrics.flops_per_sec = flops_per_sec
    exu_metrics.sfops_per_sec = sfops_per_sec

    exu_metrics.read_data = reg_read * word_size_in_bytes
    exu_metrics.write_data = reg_write * word_size_in_bytes

    # normalized performance
    # Watt = J/s
    # ops/Watt = ops/ (J/s)
    total_energy_in_pJoules = exu_metrics.energy['total']
    total_energy = total_energy_in_pJoules * 1.0e-12
    power = total_energy / total_elapsed_time_in_sec
    exu_metrics.power = power
    exu_metrics.ops_per_watt = total_ops / total_energy
    exu_metrics.iops_per_watt = total_iops / total_energy
    exu_metrics.flops_per_watt = total_flops / total_energy
    exu_metrics.sfops_per_watt = total_sfops / total_energy

    #exu_metrics.report()
    return exu_metrics
