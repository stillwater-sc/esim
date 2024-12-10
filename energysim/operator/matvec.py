import math
from typing import Any, Tuple
from numpy.random import random

from energysim.database.spm_energy import StoredProgramMachineEnergy
from energysim.execution.spm_events import StoredProgramMachineEvents
from energysim.linalg.vector import Vector
from energysim.linalg.matrix import Matrix
from energysim.execution.spm import StoredProgramMachineMetrics


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


def flat_mv_spm(rows, cols, attributes: 'StoredProgramMachineEnergy') \
        -> tuple[StoredProgramMachineEvents, StoredProgramMachineMetrics]:
    # enumerate all the energy consuming transactions for a matvec on an SPM
    spm_occurrences = StoredProgramMachineEvents()
    spm_metrics = StoredProgramMachineMetrics("Flat MV " + str(rows) + " x " + str(cols) + " SPM")

    # nr of multiply-add operations
    fmas: int = rows * cols
    spm_occurrences.fma32b = fmas

    # instructions flow through the fetch/decode/dispatch part of the pipeline
    # nr of instructions per multiply-add is roughly 13
    nr_of_instructions: int = fmas * 13
    spm_occurrences.instructions = nr_of_instructions
    spm_metrics.instruction = nr_of_instructions * attributes.instruction
    spm_occurrences.execute = fmas
    spm_metrics.execute = fmas * attributes.execute
    # we need to read two inputs for each MADD,
    # and one read for writing the result back to memory
    register_read = fmas * 3
    spm_occurrences.register_read = register_read
    spm_metrics.register_read = register_read * attributes.register_read
    # we write the output of the MADD to the register file
    # and we need to write all the inputs into the register file too
    register_write = fmas * 3
    spm_occurrences.register_write = register_write
    spm_metrics.register_write = register_read * attributes.register_write

    # flat mv assumes we are streaming to the cache without reuse
    cache_line_size = 32  # bytes
    matrix_elements = rows * cols
    vector_elements = cols
    total_elements = matrix_elements + vector_elements
    matrix_cache_lines: int = math.ceil(matrix_elements / cache_line_size)
    vector_cache_lines: int = math.ceil(vector_elements / cache_line_size)
    total_cache_lines_in: int = matrix_cache_lines + vector_cache_lines
    total_cache_lines_out: int = vector_cache_lines

    spm_occurrences.l1_read = total_cache_lines_in
    spm_metrics.l1_read = total_elements * attributes.l1_read
    spm_occurrences.l1_write = (total_cache_lines_in + total_cache_lines_out)
    spm_metrics.l1_write = (total_cache_lines_in + total_cache_lines_out) * attributes.l1_write

    spm_occurrences.l2_read = total_cache_lines_in
    spm_metrics.l2_read = total_cache_lines_in * attributes.l2_read
    spm_occurrences.l2_write = (total_cache_lines_in + total_cache_lines_out)
    spm_metrics.l2_write = (total_cache_lines_in + total_cache_lines_out) * attributes.l2_write

    spm_occurrences.l3_read = total_cache_lines_in
    spm_metrics.l3_read = total_cache_lines_in * attributes.l3_read
    spm_occurrences.l3_write = (total_cache_lines_in + total_cache_lines_out)
    spm_metrics.l3_write = (total_cache_lines_in + total_cache_lines_out) * attributes.l3_write

    # for the DRAM, we assume just the energy for reading the operands for compute,
    # and do not include the energy required for memory management
    # to get the data structures into memory
    spm_occurrences.dram_read = total_cache_lines_in
    spm_metrics.dram_read = total_cache_lines_in * attributes.dram_read
    spm_occurrences.dram_write = total_cache_lines_out
    spm_metrics.dram_write = total_cache_lines_out * attributes.dram_write

    # consolidate sets
    spm_metrics.compute = spm_metrics.instruction + spm_metrics.execute + spm_metrics.register_read + spm_metrics.register_write
    spm_metrics.l1 = spm_metrics.l1_read + spm_metrics.l1_write
    spm_metrics.l2 = spm_metrics.l2_read + spm_metrics.l2_write
    spm_metrics.l3 = spm_metrics.l3_read + spm_metrics.l3_write
    spm_metrics.cache_read = spm_metrics.l1_read + spm_metrics.l2_read + spm_metrics.l3_read
    spm_metrics.cache_write = spm_metrics.l1_write + spm_metrics.l2_write + spm_metrics.l3_write
    spm_metrics.cache = spm_metrics.cache_read + spm_metrics.cache_write
    spm_metrics.memory = spm_metrics.dram_read + spm_metrics.dram_write
    spm_metrics.data_movement = spm_metrics.cache + spm_metrics.memory
    spm_metrics.total = spm_metrics.compute + spm_metrics.data_movement

    # calculate performance metrics
    # Matvec is memory bound, which implies that
    # the number of operations are governed by number of operands we can fetch
    memory_clock = attributes.memory_clock

    # how much time would it take to pull the total number of cachelines in
    # a DDR5 DIMM is 64bit wide, so to transfer a 64byte cacheline, we need
    # 8 bus cycles, with is 4 memory clocks.
    bandwidth = attributes.memory_clock * 8 * 2
    throughput = total_cache_lines_in * attributes.cache_line_size / bandwidth
    gops = 1.0 / throughput
    spm_metrics.TIPS = gops / 100.0
    spm_metrics.TOPS = gops / 1000.0
    spm_metrics.MemGOPS = gops

    return spm_occurrences, spm_metrics
