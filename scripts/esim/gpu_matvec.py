from energysim.database.gpu_energy import GraphicsProcessingUnitEnergyDatabase
from energysim.execution.gpu_metrics import GraphicsProcessingUnitMetrics
from energysim.models.gpu_configuration import GraphicsProcessingUnitConfiguration
from energysim.models.design_category import DesignCategory
from energysim.operator.flat_matvec import flat_matvec_gpu


def sample_gpu(process_node: str, rows: int, cols: int, config: 'GraphicsProcessingUnitConfiguration') -> 'GraphicsProcessingUnitMetrics':
    db = GraphicsProcessingUnitEnergyDatabase()
    full = db.load_data('../../data/gpu_energy.csv')  # this returns a full DataFrame, but we ignore it
    locator = (full['node'] == process_node)
    selected_node = full.loc[locator]
    if selected_node is None:
        raise ValueError(f'Process {selected_node} not supported')

    base_sample = db.lookupEnergySet(process_node, config.word_size)
    print(base_sample)
    gpu_metrics = flat_matvec_gpu(rows, cols, base_sample, config)
    return gpu_metrics

def nvidia_geforce_10_gtx1070(rows: int, cols: int):
    """
        Modeling a matvec kernel on a Geforce 10 GTX 1070
    Args:
        rows: number of rows in the matrix
        cols: number of columns in the matrix

    Returns:
        a performance report
    """
    threads_per_block = 128  # threads_per_block
    blocks_per_grid = (rows + threads_per_block - 1) // threads_per_block  # blocks_per_grid
    category = DesignCategory.HighVolume
    core_clock_ghz = 1.5
    memory_clock_ghz = 2.0
    cache_line_size_in_bytes = 64
    word_size_in_bytes = 4   # 4 bytes for single precision, 2 bytes for half, and 1 byte for FP8
    memory_burst_size_in_bytes = 64 # typically can be 32b, 64b, 128bytes
    memory_channels = 8
    channel_width_in_bytes = 4 # LPDDR tends to be 2 bytes, DDR and GDDR tend to be 8 bytes, HBM is 128 bytes
        # Geforce 10 GTX 1070 had 256bits of GDDR5 memory with a 2GHz memory clock for 256GB/s memory bw

    config = GraphicsProcessingUnitConfiguration(
        category,
        core_clock_ghz,
        memory_clock_ghz,
        word_size_in_bytes,
        cache_line_size_in_bytes,
        memory_burst_size_in_bytes,
        memory_channels,
        channel_width_in_bytes,
        threads_per_block,
        blocks_per_grid
    )
    metrics = sample_gpu('n14t', rows, cols, config)
    metrics.report()

if __name__ == '__main__':
    rows = 1024*1024
    cols = 1024
    nvidia_geforce_10_gtx1070(rows, cols)


# Actual matvec kernel on a GeForce 10 GTX 1070
#
# Threads per Block : 128
# Blocks per Grid   : 8192
# Matrix-Vector Multiplication on GPU
# Dimensions    : 1048576 x 1024
# Execution Time: 72.477699 ms
# Throughput    : 14.814789 SP-GLOPS
# Matrix-Vector Multiplication on GPU with load/unload over PCIe
# Dimensions    : 1048576 x 1024
# Execution Time: 681.247375 ms
# Throughput    : 1.576141 SP-GLOPS

# Machine Configuration
# Core clock          : 1.5 GHz
# Memory clock        : 2.0 GHz
# Word size           : 4 bytes
# Cache line size     : 64 bytes
# Memory burst        : 64 bytes
# Memory channels     : 8
# Channel width       : 4 bytes
# Max Memory BW       : 256.000 GBytes
#
# Kernel Dispatch Configuration
# Threads per block   : 128
# Blocks per grid     : 8192
# Total nr of Warps   : 32768
#
# Performance summary
# Elapsed time        :  73.820 msec
# IPS                 : 290.909 GIPS/sec
# FLOPS               :  14.545 GFLOPS/sec
# Memory Transactions :  36.910 MMemory Transactions
# Memory clk          : 500.000 psec
# Data Size read      :   4.295 GBytes
# Data Size written   :   4.096 kBytes
# Memory Throughput   : 500.000 MMemT/sec
# Memory Read         :  58.182 GBytes/sec
# Memory Write        :  55.486 kBytes/sec
#
# Normalized performance
# Total FLOPS         :   1.074 GFLOPS
# Power               :  10.170 Watt
# FLOPS/Watt          : 105.577 MFLOPS/Watt

