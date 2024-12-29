from energysim import Vector, Matrix, flat_matrix_vector_multiply

def test_pattern():
    # Create a matrix
    matrix = Matrix([[1, 2, 3], [4, 5, 6]])

    # Create a vector
    vector = Vector([2, 3, 4])

    # Multiply matrix and vector
    result = flat_matrix_vector_multiply(matrix, vector)
    print(result)  # Outputs the resulting vector

if __name__ == '__main__':
    test_pattern()

