from energysim.linalg.vector import Vector
from energysim.linalg.matrix import Matrix

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

