import math
from typing import Any, Tuple
from numpy.random import random

from energysim.database.spm_energy import StoredProgramMachineEnergy
from energysim.linalg.vector import Vector
from energysim.linalg.matrix import Matrix
from energysim.execution.spm_metrics import StoredProgramMachineMetrics
from energysim.models.spm_configuration import StoredProgramMachineConfiguration


# flat matrix-vector function
def flat_matrix_vector_multiply(matrix: 'Matrix', vector: 'Vector') -> 'Vector':
    """
    Multiply a matrix with a vector

    Args:
        matrix (Matrix): Input matrix
        vector (Vector): Input vector

    Returns:
        Vector: Result of matrix-vector multiplication

    Raises:
        ValueError: If matrix columns do not match vector size
    """
    # Check dimensions
    if matrix.shape[1] != vector.size:
        raise ValueError("Matrix columns must match vector size")

    # Perform multiplication
    result_data = []
    for row in matrix[0:matrix.shape[0]]:
        # Compute dot product of matrix row and vector
        row_result = sum(row[j] * vector.get(j) for j in range(vector.size))
        result_data.append(row_result)

    return Vector(result_data)


def flat_mv_spm(rows, cols, attributes: 'StoredProgramMachineEnergy', config: 'StoredProgramMachineConfiguration') \
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
