from typing import Any

from energysim.linalg.vector import Vector
from energysim.linalg.matrix import Matrix
from energysim.models.energy import EnergyDatabase
from energysim.models.spm import StoredProgramMachineEnergy

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




def flat_mv_spm(rows, cols, energies: 'EnergyDatabase') -> 'StoredProgramMachineEnergy':
    # enumerate all the energy consuming transactions for a matvec on an SPM
    energy = StoredProgramMachineEnergy("Flat MV " + str(rows) + " x " + str(cols) + " SPM", energies)

    # nr of multiply-add operations
    nrMADDs: int | Any = rows * cols * 2

    # instructions flow through the fetch/decode/dispatch part of the pipeline
    # nr of instructions per multiply-add is roughly 13
    nrOfInstructions: int | Any = nrMADDs * 13
    energy.instruction = nrOfInstructions * energies.instruction
    energy.execute = nrMADDs * energies.execute
    # we need to read two inputs for each MADD, and one read for writing
    # the result back to memory
    energy.register_read = nrMADDs * 2 + nrMADDs
    # we write the output of the MADD to the register file
    # and we need to write all the inputs into the register file too
    energy.register_write = nrMADDs + nrMADDs * 2

    # flat mv assumes we are streaming to the cache without reuse
    cache_line_size = 32  # bytes
    matrix_elements = rows * cols
    vector_elements = cols
    matrix_cache_lines: int | Any = 1 + (matrix_elements / cache_line_size)
    vector_cache_lines: int | Any = 1 + (vector_elements / cache_line_size)
    total_cache_lines: int | Any = matrix_cache_lines + vector_cache_lines
    energy.l1_read = matrix_elements + vector_elements
    energy.l1_write = total_cache_lines
    energy.l2_read = total_cache_lines
    energy.l2_write = total_cache_lines
    energy.l3_read = total_cache_lines
    energy.l3_write = total_cache_lines
    # for the DRAM, we assume just the energy for compute, not memory management
    # to get the data structures into memory
    energy.memory_read = total_cache_lines
    energy.memory_write = total_cache_lines

    return energy
