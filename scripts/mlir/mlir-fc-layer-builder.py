import numpy as np
from mlir.ir import *
from mlir.dialects.func import *
from mlir.dialects.tosa import *
import mlir.execution_engine
from mlir.passmanager import PassManager

def create_fc_layer_ir(input_size=10, output_size=5):
    context = Context()
    
    # Create random weights and biases
    weights = np.random.randn(input_size, output_size).astype(np.float32)
    biases = np.random.randn(output_size).astype(np.float32)
    
    with context, Location.unknown():
        module = Module.create()
        
        # Create function type
        input_type = RankedTensorType.get([1, input_size], F32Type.get())
        output_type = RankedTensorType.get([1, output_size], F32Type.get())
        fn_type = FunctionType.get([input_type], [output_type])
        
        with InsertionPoint(module.body):
            @FuncOp.from_py_func(input_type)
            def fc_relu(arg):
                # Create constant for weights
                weight_type = RankedTensorType.get([input_size, output_size], F32Type.get())
                weight_attr = DenseElementsAttr.get(weights, type=weight_type)
                weight_const = Operation.create("tosa.const", 
                                             results=[weight_type],
                                             attributes={"value": weight_attr}).results[0]
                
                # Create constant for biases
                bias_type = RankedTensorType.get([output_size], F32Type.get())
                bias_attr = DenseElementsAttr.get(biases, type=bias_type)
                bias_const = Operation.create("tosa.const",
                                           results=[bias_type],
                                           attributes={"value": bias_attr}).results[0]
                
                # Create zero constant for ReLU
                zero_type = RankedTensorType.get([1, output_size], F32Type.get())
                zero_attr = DenseElementsAttr.get_splat(zero_type, FloatAttr.get(F32Type.get(), 0.0))
                zero_const = Operation.create("tosa.const",
                                           results=[zero_type],
                                           attributes={"value": zero_attr}).results[0]
                
                # Reshape bias for broadcasting
                reshape_out_type = RankedTensorType.get([1, output_size], F32Type.get())
                bias_shape = np.array([1, output_size], dtype=np.int64)
                bias_shape_attr = DenseElementsAttr.get(bias_shape)
                reshaped_bias = Operation.create(
                    "tosa.reshape",
                    results=[reshape_out_type],
                    operands=[bias_const],
                    attributes={"new_shape": bias_shape_attr}).results[0]
                
                # Matmul operation
                matmul_out_type = RankedTensorType.get([1, output_size], F32Type.get())
                matmul = Operation.create(
                    "tosa.matmul",
                    results=[matmul_out_type],
                    operands=[arg, weight_const]).results[0]
                
                # Add biases
                add_out_type = RankedTensorType.get([1, output_size], F32Type.get())
                add = Operation.create(
                    "tosa.add",
                    results=[add_out_type],
                    operands=[matmul, reshaped_bias]).results[0]
                
                # ReLU activation using maximum
                relu_out_type = RankedTensorType.get([1, output_size], F32Type.get())
                relu = Operation.create(
                    "tosa.maximum",
                    results=[relu_out_type],
                    operands=[add, zero_const]).results[0]
                
                return relu

    return module

def save_mlir_to_file(module, filename="fc_layer.mlir"):
    with open(filename, "w") as f:
        f.write(str(module))
    print(f"MLIR module has been written to {filename}")

if __name__ == "__main__":
    # Create the MLIR module
    module = create_fc_layer_ir(10, 5)
    
    # Save to file
    save_mlir_to_file(module)
