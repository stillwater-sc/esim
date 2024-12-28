from mlir.ir import *
import mlir.dialects.func as func
import mlir.dialects.math as mlir_math

with Context() as ctx, Location.unknown():
    module = Module.create()
    with InsertionPoint(module.body):
        f32_t = F32Type.get()
        @func.FuncOp.from_py_func(f32_t)
        def emit_sqrt(arg):
            assert isinstance(arg.type, F32Type)
            return mlir_math.SqrtOp(arg)

print(module)