import math

from energysim.database.spm_energy import StoredProgramMachineEnergy
from energysim.execution.spm_metrics import StoredProgramMachineMetrics
from energysim.models.spm_configuration import StoredProgramMachineConfiguration


# flat matrix-matrix operator on a Stored Program Machine
def flat_matmul_spm(M, N, K, attributes: 'StoredProgramMachineEnergy', config: 'StoredProgramMachineConfiguration') \
        -> 'StoredProgramMachineMetrics':
    # enumerate all the energy consuming transactions for a matmul on an SPM
    spm_metrics = StoredProgramMachineMetrics("Flat Matmul " + str(M) + " x " + str(N) + " x " + str(K) + " SPM")

    # nr of multiply-add operations
    fmas: int = M * N * K
    spm_metrics.record('fma', fmas, attributes.fma32b)
    spm_metrics.record('execute', fmas, attributes.fma32b)

    # instructions flow through the fetch/decode/dispatch part of the pipeline
    # nr of instructions per multiply-add is roughly 13
    nr_of_instructions: int = fmas * 13
    spm_metrics.record('instruction', nr_of_instructions, attributes.instruction)

    # we need to read two inputs for each fma,
    # and one read for writing the result back to memory
    register_read = fmas * 3
    spm_metrics.record('register_read', register_read, attributes.register_read)
    # we write the output of the fmas to the register file
    # and we need to write all the inputs into the register file too
    register_write = fmas * 3
    spm_metrics.record('register_write', register_write, attributes.register_write)

    # flat mv assumes we are streaming to the cache without reuse
    cache_line_size = 32  # bytes
    A_matrix_elements = M * N
    B_matrix_elements = N * K
    C_matrix_elements = M * K
    total_elements = A_matrix_elements + B_matrix_elements + C_matrix_elements
    A_matrix_cache_lines: int = math.ceil(A_matrix_elements / cache_line_size)
    B_matrix_cache_lines: int = math.ceil(B_matrix_elements / cache_line_size)
    C_matrix_cache_lines: int = math.ceil(C_matrix_elements / cache_line_size)
    total_cache_lines_in: int = A_matrix_cache_lines + B_matrix_cache_lines + C_matrix_cache_lines
    total_cache_lines_out: int = C_matrix_cache_lines
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
    memory_clock = config.memory_clock

    # how much time would it take to pull the total number of cachelines in
    # a DDR5 DIMM is 64bit wide, so to transfer a 64byte cacheline, we need
    # 8 bus cycles, with is 4 memory clocks.
    bandwidth = memory_clock * 8 * 2
    throughput = total_cache_lines_in * config.cache_line_size / bandwidth
    gops = 1.0 / throughput
    spm_metrics.TIPS = gops / 100.0
    spm_metrics.TOPS = gops / 1000.0
    spm_metrics.MemGOPS = gops

    return spm_metrics
