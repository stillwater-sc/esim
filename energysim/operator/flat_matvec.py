import math

from energysim.database.dfa_energy import DomainFlowArchitectureEnergy
from energysim.database.spm_energy import StoredProgramMachineEnergy
from energysim.execution.dfa_metrics import DomainFlowArchitectureMetrics
from energysim.execution.exu_metrics import ExecutionUnitMetrics
from energysim.execution.gpu_metrics import GraphicsProcessingUnitMetrics
from energysim.execution.spm_metrics import StoredProgramMachineMetrics
from energysim.models.exu_configuration import ExecutionUnitConfiguration
from energysim.models.spm_configuration import StoredProgramMachineConfiguration

# flat matrix-vector operator on a raw Execution Unit
def flat_matvec_exu(rows, cols, attributes: 'ExecutionUnitEnergy', config: 'ExecutionUnitConfiguration') \
        -> 'ExecutionUnitMetrics':
    # enumerate all the energy consuming transactions for a matvec on an SPM
    exu_metrics = ExecutionUnitMetrics("Flat MV " + str(rows) + " x " + str(cols) + " EXU")

    # nr of multiply-add operations
    fmas: int = rows * cols
    exu_metrics.record('agu', 3*fmas, attributes.agu)   # need to generate addresses for 2 input operands and 1 output operand
    exu_metrics.record('alu', rows*cols + rows, attributes.alu)     # loop control iteration variables for double loop matvec
    exu_metrics.record('fpu', fmas, attributes.fpu)     # actual number of FMAs of the workload
    exu_metrics.record('sfu', 0, attributes.sfu) # no SFU operations for matvec

    # we need to read two inputs for each fma,
    # and one read for writing the result back to memory
    reg_read = fmas * 3
    exu_metrics.record('reg_read', reg_read, attributes.reg_read)
    # we write the output of the fma to the register file
    # and we need to write all the inputs into the register file too
    reg_write = fmas * 3
    exu_metrics.record('reg_write', reg_write, attributes.reg_write)

    # consolidate sets
    exu_metrics.consolidate('compute', ['agu', 'alu', 'fpu', 'sfu'])
    exu_metrics.consolidate('data', ['reg_read', 'reg_write'])
    exu_metrics.consolidate('total', ['compute', 'data'])

    # calculate performance metrics

    # instruction throughput

    total_iops = exu_metrics.events['agu'] + exu_metrics.events['alu']
    total_flops = exu_metrics.events['fpu']
    total_sfops = exu_metrics.events['sfu']
    total_ops = total_iops + total_flops + total_sfops
    exu_metrics.total_iops = total_iops
    exu_metrics.total_flops = total_flops
    exu_metrics.total_sfops = total_sfops
    exu_metrics.total_ops = total_ops
    # assume that the pipeline has enough AGU and ALU throughput to saturate the FPU
    total_elapsed_time_in_sec = total_flops * config.clock_cycle_ns * 1.0e-9
    exu_metrics.elapsed_time = total_elapsed_time_in_sec

    ops_per_sec = total_ops / total_elapsed_time_in_sec
    iops_per_sec = total_iops / total_elapsed_time_in_sec
    flops_per_sec = total_flops / total_elapsed_time_in_sec
    sfops_per_sec = total_sfops / total_elapsed_time_in_sec
    exu_metrics.ops_per_sec = ops_per_sec
    exu_metrics.iops_per_sec = iops_per_sec
    exu_metrics.flops_per_sec = flops_per_sec
    exu_metrics.sfops_per_sec = sfops_per_sec

    exu_metrics.read_data = reg_read * config.word_size
    exu_metrics.write_data = reg_write * config.word_size

    # copy the machine attributes into the metrics data structure
    exu_metrics.core_clock_ghz = config.core_clock
    exu_metrics.word_size = config.word_size
    exu_metrics.agus = config.agus
    exu_metrics.alus = config.alus
    exu_metrics.fpus = config.fpus
    exu_metrics.sfus = config.sfus

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

    return exu_metrics

# flat matrix-vector operator on a Stored Program Machine
def flat_matvec_spm(rows, cols, attributes: 'StoredProgramMachineEnergy', config: 'StoredProgramMachineConfiguration') \
        -> 'StoredProgramMachineMetrics':
    # enumerate all the energy consuming transactions for a matvec on an SPM
    spm_metrics = StoredProgramMachineMetrics("Flat MV " + str(rows) + " x " + str(cols) + " SPM")

    # nr of multiply-add operations
    fmas: int = rows * cols
    spm_metrics.record('fma', fmas, attributes.fma32b)
    spm_metrics.record('execute', fmas, attributes.fma32b)

    # instructions flow through the fetch/decode/dispatch part of the pipeline
    # nr of instructions per multiply-add is roughly 13
    nr_of_instructions: int = fmas * 6
    spm_metrics.record('instruction', nr_of_instructions, attributes.instruction)

    # we need to read two inputs for each fma,
    # and one read for writing the result back to memory
    register_read = fmas * 3
    spm_metrics.record('register_read', register_read, attributes.register_read)
    # we write the output of the MADD to the register file
    # and we need to write all the inputs into the register file too
    register_write = fmas * 3
    spm_metrics.record('register_write', register_write, attributes.register_write)

    # flat mv assumes we are streaming to the cache without reuse
    cache_line_size = config.cache_line_size  # bytes
    memory_burst_size = config.memory_burst_size # bytes
    matrix_elements = rows * cols
    vector_elements = cols
    total_elements = matrix_elements + vector_elements
    matrix_data_structure_size = matrix_elements * config.word_size
    vector_data_structure_size = vector_elements * config.word_size
    total_data_structure_size = total_elements * config.word_size
    matrix_cache_lines: int = math.ceil(matrix_data_structure_size / cache_line_size)
    vector_cache_lines: int = math.ceil(vector_data_structure_size / cache_line_size)
    total_cache_lines_in: int = matrix_cache_lines + vector_cache_lines
    total_cache_lines_out: int = vector_cache_lines
    total_cache_lines: int = (total_cache_lines_in + total_cache_lines_out)

    spm_metrics.record('l1_read', fmas*2, attributes.l1_read)
    spm_metrics.record('l1_write', total_cache_lines, attributes.l1_write)

    spm_metrics.record('l2_read', total_cache_lines_in, attributes.l2_read)
    spm_metrics.record('l2_write', total_cache_lines, attributes.l2_write)

    spm_metrics.record('l3_read', total_cache_lines_in, attributes.l3_read)
    spm_metrics.record('l3_write', total_cache_lines, attributes.l3_write)

    # for the DRAM, we assume just the energy for reading the operands for compute,
    # and do not include the energy required for memory management
    # to get the data structures into memory
    spm_metrics.record('dram_read', total_cache_lines_in, attributes.dram_read)
    spm_metrics.record('dram_write', total_cache_lines_out, attributes.dram_write)

    # consolidate sets
    spm_metrics.consolidate('compute', ['instruction', 'execute', 'register_read', 'register_write'])
    spm_metrics.consolidate('l1', ['l1_read', 'l1_write'])
    spm_metrics.consolidate('l2', ['l2_read', 'l2_write'])
    spm_metrics.consolidate('l3', ['l3_read', 'l3_write'])
    spm_metrics.consolidate('cache_read', ['l1_read', 'l2_read', 'l3_read'])
    spm_metrics.consolidate('cache_write', ['l1_write', 'l2_write', 'l3_write'])
    spm_metrics.consolidate('cache', ['cache_read', 'cache_write'])
    spm_metrics.consolidate('memory', ['dram_read', 'dram_write'])
    spm_metrics.consolidate('data_movement', ['cache', 'memory'])
    spm_metrics.consolidate('total', ['compute', 'data_movement'])

    # calculate performance metrics
    # Matvec is memory bound, which implies that
    # the number of operations are governed by number of operands we can fetch

    # how long would it take to move the total number of data from and to the memory
    # a 64bit DDR DIMM needs 4 clocks to move a cacheline
    memory_transactions = total_cache_lines
    total_elapsed_time_in_sec = memory_transactions * 4 * config.memory_cycle_ns * 1.0e-9

    # instruction throughput yielded
    total_instructions = spm_metrics.events['instruction']
    instr_per_sec = total_instructions / total_elapsed_time_in_sec
    total_flops = spm_metrics.events['execute']
    flops_per_sec = total_flops / total_elapsed_time_in_sec
    memory_ops_per_second = total_cache_lines / total_elapsed_time_in_sec

    spm_metrics.elapsed_time = total_elapsed_time_in_sec
    spm_metrics.instr_per_sec = instr_per_sec
    spm_metrics.flops_per_sec = flops_per_sec
    spm_metrics.memory_transactions = memory_transactions
    spm_metrics.memory_clock_ns = config.memory_cycle_ns
    spm_metrics.read_data = total_cache_lines_in * cache_line_size
    spm_metrics.write_data = total_cache_lines_out * cache_line_size
    spm_metrics.memory_read_bw = spm_metrics.read_data / total_elapsed_time_in_sec
    spm_metrics.memory_write_bw = spm_metrics.write_data / total_elapsed_time_in_sec
    spm_metrics.memops_per_sec = memory_ops_per_second

    # copy the machine attributes into the metrics data structure
    spm_metrics.core_clock_ghz = config.core_clock
    spm_metrics.memory_clock_ghz = config.memory_clock
    spm_metrics.word_size = config.word_size
    spm_metrics.cache_line_size = config.cache_line_size
    spm_metrics.memory_burst = config.memory_burst_size
    spm_metrics.memory_channels = config.memory_channels
    spm_metrics.channel_width = config.channel_width

    # normalized performance
    # Watt = J/s
    # gops/Watt = gops/ (J/s)
    total_energy_in_pJoules = spm_metrics.energy['total']
    total_energy = total_energy_in_pJoules * 1.0e-12
    power = total_energy / total_elapsed_time_in_sec
    spm_metrics.total_flops = total_flops
    spm_metrics.power = power
    spm_metrics.flops_per_watt = total_flops / power

    return spm_metrics


# flat matrix-vector operator on an NVIDIA Graphics Processing Unit
def flat_matvec_gpu(rows, cols, energies: 'GraphicsProcessingUnitEnergy', config: 'GraphicsProcessingUnitConfiguration') \
        -> 'GraphicsProcessingUnitMetrics':
    # enumerate all the energy consuming transactions for a matvec on a GPU
    gpu_metrics = GraphicsProcessingUnitMetrics("Flat MV " + str(rows) + " x " + str(cols) + " GPU")

    # nr of multiply-add operations
    fmas: int = rows * cols
    gpu_metrics.record('fma', fmas, energies.fma32b)
    gpu_metrics.record('execute', fmas, energies.fma32b)

    # instructions flow through the fetch/decode/dispatch part of the pipeline
    # nr of instructions per multiply-add is roughly 20
    nr_of_instructions: int = fmas * 20
    gpu_metrics.record('instruction', nr_of_instructions, energies.instruction)

    # we need to read two inputs for each fma,
    # and one read for writing the result back to memory
    register_read = fmas * 3
    gpu_metrics.record('register_read', register_read, energies.reg_read)
    # we write the output of the fma to the register file
    # and we need to write all the inputs into the register file too
    register_write = fmas * 3
    gpu_metrics.record('register_write', register_write, energies.reg_write)

    # flat mv assumes we are streaming to the cache without reuse
    threads_per_block = config.threads_per_block
    blocks_per_grid = config.blocks_per_grid
    gpu_metrics.threads_per_block = threads_per_block
    gpu_metrics.blocks_per_grid = blocks_per_grid

    matrix_elements = rows * cols
    vector_elements = cols
    total_elements = matrix_elements + vector_elements
    matrix_data_structure_size = matrix_elements * config.word_size
    vector_data_structure_size = vector_elements * config.word_size
    total_data_structure_size = total_elements * config.word_size

    # a decoded instruction is sent to all the ALUs via a Warp (NVIDIA) or Wavefront (AMD) scheduler
    # this is an energetic event and needs to be tracked
    # we are assuming a flat matvec kernel that is laid out on a 1D grid where each
    # thread takes care of one element of the result vector
    nr_of_warps: int = math.ceil(rows / 32)
    gpu_metrics.nr_of_warps = nr_of_warps

    gpu_metrics.record('l1_read', fmas * 2, energies.l1_read)
    gpu_metrics.record('l1_write', fmas, energies.l1_write)

    # the vector elements are managed in the shared memory to avoid overfetching to global memory
    gpu_metrics.record('smem_read', fmas, energies.smem_read)
    gpu_metrics.record('smem_write', 2 * cols, energies.smem_write)

    # for the DRAM, we assume just the energy for reading the operands for compute,
    # and do not include the energy required for memory management
    # to get the data structures into memory

    # modeling the efficiency of the memory traffic through an occupancy
    # if we have 100% occupancy, we do not over fetch
    # if we have 75% occupancy, we need to fetch 25% more: (1.0 + (1.0 - occupancy))
    memory_burst_occupancy: float = 0.9   # each memory burst has 90% valid data
    overfetch_factor = (1.0 + (1.0 - memory_burst_occupancy))
    total_memory_reads = total_elements * overfetch_factor
    total_memory_read_bursts = math.ceil(total_memory_reads / config.memory_burst_size)
    total_memory_writes = rows / config.memory_burst_size * overfetch_factor
    total_memory_write_bursts = math.ceil(total_memory_writes / config.memory_burst_size)  # each row is an element of the result vector
    gpu_metrics.record('gmem_read', total_memory_read_bursts, energies.gmem_read)
    gpu_metrics.record('gmem_write', total_memory_write_bursts, energies.gmem_write)

    # consolidate sets
    gpu_metrics.consolidate('compute', ['instruction', 'execute', 'register_read', 'register_write'])
    gpu_metrics.consolidate('l1', ['l1_read', 'l1_write'])
    gpu_metrics.consolidate('smem', ['smem_read', 'smem_write'])
    gpu_metrics.consolidate('gmem', ['gmem_read', 'gmem_write'])
    gpu_metrics.consolidate('cache_read', ['l1_read', 'smem_read'])
    gpu_metrics.consolidate('cache_write', ['l1_write', 'smem_write'])
    gpu_metrics.consolidate('cache', ['cache_read', 'cache_write'])
    gpu_metrics.consolidate('memory', ['gmem_read', 'gmem_write'])
    gpu_metrics.consolidate('data_movement', ['cache', 'memory'])
    gpu_metrics.consolidate('total', ['compute', 'data_movement'])

    # calculate performance metrics
    # Matvec is memory bound, which implies that
    # the number of operations are governed by number of operands we can fetch

    # how long would it take to move the total number of data from and to the memory
    # a 64bit DDR DIMM needs 4 clocks to move a cacheline
    memory_transactions = total_memory_read_bursts + total_memory_read_bursts
    total_elapsed_time_in_sec = memory_transactions * 4 * config.memory_cycle_ns * 1.0e-9

    # instruction throughput yielded
    total_instructions = gpu_metrics.events['instruction']
    instr_per_sec = total_instructions / total_elapsed_time_in_sec
    total_flops = gpu_metrics.events['execute']
    flops_per_sec = total_flops / total_elapsed_time_in_sec
    memory_ops_per_second = memory_transactions / total_elapsed_time_in_sec

    gpu_metrics.elapsed_time = total_elapsed_time_in_sec
    gpu_metrics.instr_per_sec = instr_per_sec
    gpu_metrics.flops_per_sec = flops_per_sec
    gpu_metrics.memory_transactions = memory_transactions
    gpu_metrics.memory_clock_ns = config.memory_cycle_ns
    gpu_metrics.read_data = matrix_data_structure_size
    gpu_metrics.write_data = vector_data_structure_size
    gpu_metrics.memory_read_bw = matrix_data_structure_size / total_elapsed_time_in_sec
    gpu_metrics.memory_write_bw = vector_data_structure_size / total_elapsed_time_in_sec
    gpu_metrics.memops_per_sec = memory_ops_per_second

    # copy the machine attributes into the metrics data structure
    gpu_metrics.core_clock_ghz = config.core_clock
    gpu_metrics.memory_clock_ghz = config.memory_clock
    gpu_metrics.word_size = config.word_size
    gpu_metrics.cache_line_size = config.cache_line_size
    gpu_metrics.memory_burst = config.memory_burst_size
    gpu_metrics.memory_channels = config.memory_channels
    gpu_metrics.channel_width = config.channel_width
    # peak memory bandwidth
    gpu_metrics.max_memory_bw = config.memory_clock * 2 * config.channel_width * config.memory_channels * 2 * 1.0e9

    # normalized performance
    # Watt = J/s
    # flops/Watt = flops/ (J/s)
    total_energy_in_pJoules = gpu_metrics.energy['total']
    total_energy = total_energy_in_pJoules * 1.0e-12
    power =  total_energy / total_elapsed_time_in_sec
    gpu_metrics.total_flops = total_flops
    gpu_metrics.power = power
    gpu_metrics.flops_per_watt = total_flops / power

    return gpu_metrics


class DomainFlowArchitectureConfiguration:
    pass


def flat_matvec_dfa(rows, cols, energies: DomainFlowArchitectureEnergy, config: DomainFlowArchitectureConfiguration) \
        -> DomainFlowArchitectureMetrics:
    # enumerate all the energy consuming transactions for a matvec on a DFA
    dfa_metrics = DomainFlowArchitectureMetrics("Flat MV " + str(rows) + " x " + str(cols) + " GPU")

    # nr of multiply-add operations
    fmas: int = rows * cols
    dfa_metrics.record('fma', fmas, energies.fma32b)
    dfa_metrics.record('execute', fmas, energies.fma32b)

    return dfa_metrics