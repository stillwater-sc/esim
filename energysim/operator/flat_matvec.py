import math

from energysim.database.spm_energy import StoredProgramMachineEnergy
from energysim.execution.gpu_metrics import GraphicsProcessingUnitMetrics
from energysim.execution.spm_metrics import StoredProgramMachineMetrics
from energysim.models.spm_configuration import StoredProgramMachineConfiguration


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
    nr_of_instructions: int = fmas * 13
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
    cache_line_size = 32  # bytes
    matrix_elements = rows * cols
    vector_elements = cols
    total_elements = matrix_elements + vector_elements
    matrix_cache_lines: int = math.ceil(matrix_elements / cache_line_size)
    vector_cache_lines: int = math.ceil(vector_elements / cache_line_size)
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
    total_latency = total_cache_lines * 4 * config.memory_cycle_ns

    # instruction throughput yielded
    gips = spm_metrics.events['instruction'] / total_latency
    gops = spm_metrics.events['execute'] / total_latency
    memory_gops = total_cache_lines / total_latency

    spm_metrics.TIPS = gips / 1000.0
    spm_metrics.TOPS = gops / 1000.0
    spm_metrics.MemGOPS = memory_gops

    return spm_metrics


# flat matrix-vector operator on an NVIDIA Graphics Processing Unit
def flat_matvec_gpu(rows, cols, attributes: 'GraphicsProcessingUnitEnergy', config: 'GraphicsProcessingUnitConfiguration') \
        -> 'GraphicsProcessingUnitMetrics':
    # enumerate all the energy consuming transactions for a matvec on a GPU
    gpu_metrics = GraphicsProcessingUnitMetrics("Flat MV " + str(rows) + " x " + str(cols) + " GPU")

    # nr of multiply-add operations
    fmas: int = rows * cols
    gpu_metrics.record('fma', fmas, attributes.fma32b)
    gpu_metrics.record('execute', fmas, attributes.fma32b)

    # instructions flow through the fetch/decode/dispatch part of the pipeline
    # nr of instructions per multiply-add is roughly 20
    nr_of_instructions: int = fmas * 20
    gpu_metrics.record('instruction', nr_of_instructions, attributes.instruction)

    # we need to read two inputs for each fma,
    # and one read for writing the result back to memory
    register_read = fmas * 3
    gpu_metrics.record('register_read', register_read, attributes.register_read)
    # we write the output of the fma to the register file
    # and we need to write all the inputs into the register file too
    register_write = fmas * 3
    gpu_metrics.record('register_write', register_write, attributes.register_write)

    # flat mv assumes we are streaming to the cache without reuse
    threads_per_block = config.threads_per_block
    blocks_per_grid = config.blocks_per_grid
    matrix_elements = rows * cols
    vector_elements = cols
    total_elements = matrix_elements + vector_elements

    # a decoded instruction is sent to all the ALUs via a Warp (NVIDIA) or Wavefront (AMD) scheduler
    # this is an energetic event and needs to be tracked
    # we are assuming a flat matvec kernel that is laid out on a 1D grid where each
    # thread takes care of one element of the result vector
    nr_of_warps: int = math.ceil(rows / 32)


    gpu_metrics.record('l1_read', fmas*2, attributes.l1_read)
    gpu_metrics.record('l1_write', fmas, attributes.l1_write)

    # the vector elements are managed in the shared memory to avoid overfetching to global memory
    gpu_metrics.record('smem_read', fmas, attributes.smem_read)
    gpu_metrics.record('smem_write', 2*cols, attributes.smem_write)

    # for the DRAM, we assume just the energy for reading the operands for compute,
    # and do not include the energy required for memory management
    # to get the data structures into memory

    # modeling the efficiency of the memory traffic through an occupancy
    # if we have 100% occupancy, we do not over fetch
    # if we have 75% occupancy, we need to fetch 25% more: (1.0 + (1.0 - occupancy))
    memory_burst_occupancy: float = 1.0   # each memory burst has 80% valid data
    overfetch_factor = (1.0 + (1.0 - memory_burst_occupancy))
    total_memory_reads = total_elements * overfetch_factor
    total_memory_read_bursts = math.ceil(total_memory_reads / config.memory_burst_size)
    total_memory_writes = rows / config.memory_burst_size * overfetch_factor
    total_memory_write_bursts = math.ceil(total_memory_writes / config.memory_burst_size)  # each row is an element of the result vector
    gpu_metrics.record('gmem_read', total_memory_read_bursts, attributes.gmem_read)
    gpu_metrics.record('gmem_write', total_memory_write_bursts, attributes.gmem_write)

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
    total_memory_bursts = total_memory_read_bursts + total_memory_read_bursts
    total_latency = total_memory_bursts * 4 * config.memory_cycle_ns

    # instruction throughput yielded
    gips = gpu_metrics.events['instruction'] / total_latency
    gops = gpu_metrics.events['execute'] / total_latency
    memory_gops = total_memory_bursts / total_latency

    gpu_metrics.TIPS = gips / 1000.0
    gpu_metrics.TOPS = gops / 1000.0
    gpu_metrics.MemGOPS = memory_gops

    return gpu_metrics
