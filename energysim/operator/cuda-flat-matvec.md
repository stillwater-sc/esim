Claude.ai

A CUDA program that performs matrix-vector multiplication. I'll write a complete example that demonstrates the key steps of CUDA matrix-vector product computation.



```cpp
#include <cuda_runtime.h>
#include <stdio.h>

// CUDA kernel for matrix-vector multiplication
__global__ void matrixVectorMulKernel(float *matrix, float *vector, float *result, 
                                       int rows, int cols) {
    // Calculate the row index for this thread
    int row = blockIdx.x * blockDim.x + threadIdx.x;
    
    // Check if the thread is within matrix row bounds
    if (row < rows) {
        float sum = 0.0f;
        
        // Compute dot product for this row
        for (int col = 0; col < cols; col++) {
            sum += matrix[row * cols + col] * vector[col];
        }
        
        // Store the result
        result[row] = sum;
    }
}

// Host function to set up and launch CUDA kernel
void matrixVectorMul(float *h_matrix, float *h_vector, float *h_result, 
                     int rows, int cols) {
    float *d_matrix, *d_vector, *d_result;
    size_t matrix_size = rows * cols * sizeof(float);
    size_t vector_size = cols * sizeof(float);
    size_t result_size = rows * sizeof(float);

    // Allocate device memory
    cudaMalloc(&d_matrix, matrix_size);
    cudaMalloc(&d_vector, vector_size);
    cudaMalloc(&d_result, result_size);

    // Copy input data to device
    cudaMemcpy(d_matrix, h_matrix, matrix_size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_vector, h_vector, vector_size, cudaMemcpyHostToDevice);

    // Configure grid and block dimensions
    int threadsPerBlock = 256;
    int blocksPerGrid = (rows + threadsPerBlock - 1) / threadsPerBlock;

    // Launch kernel
    matrixVectorMulKernel<<<blocksPerGrid, threadsPerBlock>>>(
        d_matrix, d_vector, d_result, rows, cols
    );

    // Copy result back to host
    cudaMemcpy(h_result, d_result, result_size, cudaMemcpyDeviceToHost);

    // Free device memory
    cudaFree(d_matrix);
    cudaFree(d_vector);
    cudaFree(d_result);
}

int main() {
    // Example matrix and vector dimensions
    const int rows = 4;
    const int cols = 3;

    // Host memory allocation
    float h_matrix[rows * cols] = {
        1.0f, 2.0f, 3.0f,
        4.0f, 5.0f, 6.0f,
        7.0f, 8.0f, 9.0f,
        10.0f, 11.0f, 12.0f
    };

    float h_vector[cols] = {
        1.0f, 2.0f, 3.0f
    };

    float h_result[rows];

    // Perform matrix-vector multiplication
    matrixVectorMul(h_matrix, h_vector, h_result, rows, cols);

    // Print results
    printf("Result vector:\n");
    for (int i = 0; i < rows; i++) {
        printf("%f\n", h_result[i]);
    }

    return 0;
}

```

This CUDA program demonstrates a matrix-vector product implementation with the following key components:

1. `matrixVectorMulKernel`: A CUDA kernel that performs the actual computation on the GPU
   - Each thread handles one row of the matrix
   - Computes dot product between a matrix row and the input vector
   - Stores the result in the output vector

2. `matrixVectorMul`: A host function that manages:
   - Memory allocation on the device
   - Copying input data to the GPU
   - Configuring and launching the kernel
   - Copying results back to the host
   - Cleaning up device memory

3. `main()`: Provides a simple example with:
   - A 4x3 matrix
   - A 3-element vector
   - Prints the resulting vector after multiplication

To compile this program, you'll need the NVIDIA CUDA Compiler (nvcc). A typical compilation command would be:
```
nvcc matrix_vector_product.cu -o matrix_vector_product
```

Note: This is a basic implementation. For large matrices, you might want to optimize the kernel with techniques like shared memory or vector loading.

Would you like me to explain any part of the CUDA implementation in more detail?