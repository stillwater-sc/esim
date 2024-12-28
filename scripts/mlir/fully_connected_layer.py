import numpy as np


def generate_mlir_fc_layer(input_size=10, output_size=5, filename="fc_layer.mlir"):
    # Create random weights and biases
    weights = np.random.randn(input_size, output_size).astype(np.float32)
    biases = np.random.randn(output_size).astype(np.float32)

    # Start building MLIR code
    mlir_code = ("""module {{
  func.func @fc_relu(%arg0: tensor<1x{input_size}xf32>) -> tensor<1x{output_size}xf32> {{
    %weights = arith.constant dense<{weights}> : tensor<{input_size}x{output_size}xf32>
    %biases = arith.constant dense<{biases}> : tensor<{output_size}xf32>

    // Fully connected layer (matrix multiplication)
    %0 = "tosa.matmul"(%arg0, %weights) : (tensor<1x{input_size}xf32>, tensor<{input_size}x{output_size}xf32>) -> tensor<1x{output_size}xf32>

    // Add biases
    %1 = "tosa.add"(%0, %biases) : (tensor<1x{output_size}xf32>, tensor<{output_size}xf32>) -> tensor<1x{output_size}xf32>

    // ReLU activation
    %2 = "tosa.maximum"(%1, %zero) : (tensor<1x{output_size}xf32>, tensor<1x{output_size}xf32>) -> tensor<1x{output_size}xf32>

    return %2 : tensor<1x{output_size}xf32>
  }}
}}""".format(
        input_size=input_size,
        output_size=output_size,
        weights=weights.tolist(),
        biases=biases.tolist()
    ))

    # Write to file
    with open(filename, "w") as f:
        f.write(mlir_code)

    print(f"MLIR code has been written to {filename}")


def generate_mlir_fc_layer2(input_size=10, output_size=5, filename="fc_layer.mlir"):
    # Create random weights and biases
    weights = np.random.randn(input_size, output_size).astype(np.float32)
    biases = np.random.randn(output_size).astype(np.float32)

    # Start building MLIR code
    mlir_code = """module attributes {{toy.const_fold_all = true}} {{
  func.func @fc_relu(%arg0: tensor<1x{input_size}xf32>) -> tensor<1x{output_size}xf32> {{
    // Constants for weights and biases
    %weights = "tosa.const"() {{
      value = dense<{weights}> : tensor<{input_size}x{output_size}xf32>
    }} : () -> tensor<{input_size}x{output_size}xf32>

    %biases = "tosa.const"() {{
      value = dense<{biases}> : tensor<{output_size}xf32>
    }} : () -> tensor<{output_size}xf32>

    // Zero constant for ReLU
    %zero = "tosa.const"() {{
      value = dense<0.0> : tensor<1x{output_size}xf32>
    }} : () -> tensor<1x{output_size}xf32>

    // Reshape bias for broadcasting
    %bias_reshape = "tosa.reshape"(%biases) {{
      new_shape = array<i64: 1, {output_size}>
    }} : (tensor<{output_size}xf32>) -> tensor<1x{output_size}xf32>

    // Fully connected layer implementation using TOSA ops
    %0 = "tosa.matmul"(%arg0, %weights) {{
      quantization_info = {{}}
    }} : (tensor<1x{input_size}xf32>, tensor<{input_size}x{output_size}xf32>) -> tensor<1x{output_size}xf32>

    // Add biases with proper broadcasting
    %1 = "tosa.add"(%0, %bias_reshape) : (tensor<1x{output_size}xf32>, tensor<1x{output_size}xf32>) -> tensor<1x{output_size}xf32>

    // ReLU activation using TOSA maximum
    %2 = "tosa.maximum"(%1, %zero) : (tensor<1x{output_size}xf32>, tensor<1x{output_size}xf32>) -> tensor<1x{output_size}xf32>

    return %2 : tensor<1x{output_size}xf32>
  }}
}}
""".format(
        input_size=input_size,
        output_size=output_size,
        weights=weights.tolist(),
        biases=biases.tolist()
    )

    # Write to file
    with open(filename, "w") as f:
        f.write(mlir_code)

    print(f"MLIR code has been written to {filename}")

if __name__ == "__main__":
    # Generate MLIR code for a fully connected layer with 10 inputs and 5 outputs
    generate_mlir_fc_layer2(10, 5)