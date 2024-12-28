
import mlir.ir as ir
import mlir.runtime as rt
import mlir.execution_engine as ee

print('Content of mlir.ir package')
print(dir(ir))
print(dir(ir.Context))
print('Content of mlir.runtime package')
print(dir(rt))
print('Content of mlir.execution_engine package')
print(dir(ee))
exit(1)

# Create a context
context = ir.Context()

# Create a module
module = ir.Module.create(context)

# Create a location (optional)
loc = ir.Location.unknown(context)

# Define the input and output types
input_type = ir.RankedTensorType.get([1, 10], ir.F32Type())
weight_type = ir.RankedTensorType.get([10, 20], ir.F32Type())
bias_type = ir.RankedTensorType.get([20], ir.F32Type())
output_type = ir.RankedTensorType.get([1, 20], ir.F32Type())

# Create the dense layer operation
dense_op = ir.Operation.create(
    "my_dialect.dense",
    [input_type, weight_type, bias_type],
    [output_type],
    loc
)

# Create the activation operation (e.g., ReLU)
relu_op = ir.Operation.create(
    "my_dialect.relu",
    [output_type],
    [output_type],
    loc
)

# Add operations to the module
module.body.append(dense_op)
module.body.append(relu_op)

# Print the MLIR code
print(module)