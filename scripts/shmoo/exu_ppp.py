import pandas as pd
from fontTools.ttLib.tables.E_B_D_T_ import ebdt_bitmap_format_9
from matplotlib import pyplot as plt

from energysim.database.gpu_energy import GraphicsProcessingUnitEnergyDatabase
from energysim.database.spm_energy import StoredProgramMachineEnergyDatabase, StoredProgramMachineEnergy
from energysim.execution.spm_metrics import StoredProgramMachineMetrics
from energysim.models.design_category import DesignCategory
from energysim.models.execute_unit import execute_unit
from energysim.models.gpu_configuration import GraphicsProcessingUnitConfiguration
from energysim.models.spm_configuration import StoredProgramMachineConfiguration
from energysim.operator.flat_matvec import flat_matvec_spm, flat_matvec_gpu


def spm_matvec() -> StoredProgramMachineMetrics:
    db = StoredProgramMachineEnergyDatabase()
    full = db.load_data('../../data/spm_energy.csv')
    spm_energies = db.lookupEnergySet('n05t', 64)
    print(spm_energies)

    # setup workload and hardware configuration
    rows = 1024*1024
    cols = 1024
    core_clock = 2.5 # GHz
    memory_clock = 3.2 # 3.2 GHz
    cache_line_size = 64 # bytes
    memory_burst_size = 64 # bytes
    word_size = 4 # bytes
    memory_channels = 1
    channel_width = 8 # bytes  typical DDR channel is 64bit == 8 bytes
    spm_config = StoredProgramMachineConfiguration(
        DesignCategory.HighVolume,
        core_clock,
        memory_clock,
        word_size,
        cache_line_size,
        memory_burst_size,
        memory_channels,
        channel_width
    )
    spm_metrics = flat_matvec_spm(rows, cols, spm_energies, spm_config)
    #spm_metrics.report()
    return spm_metrics

def gpu_matvec():
    """
        Modeling a matvec kernel on a Geforce 10 GTX 1070
    Args:
        rows: number of rows in the matrix
        cols: number of columns in the matrix

    Returns:
        a performance report
    """
    db = GraphicsProcessingUnitEnergyDatabase()
    full = db.load_data('../../data/gpu_energy.csv')  # this returns a full DataFrame, but we ignore it
    gpu_energies = db.lookupEnergySet('n05t', 4)
    print(gpu_energies)

    # setup workload and hardware configuration
    rows = 1024*1024
    cols = 1024
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
    gpu_metrics = flat_matvec_gpu(rows, cols, gpu_energies, config)
    return gpu_metrics


if __name__ == '__main__':
    """
    Generate a performance/Watt scatter plot for different data path configurations.
    
    we have 
    - single execute unit, like an ALU or FPU that is part of a Stored Program Machine
    - SIMD unit
    - vector unit
    - matrix unit
    - systolic array
    
    those would represent that 'raw' silicon capability of the compute core
    when we then wrap them into the resource contention management control algorith
    this will derate these performance/power densities due to all the control machinery
    required to move the data
    
    start with the basics
    ALU = 1TOPS/Watt  = nr of ops/sec / J/sec = ops/J    
    example: 1000 ops / 2374 pJ = 1.0e3 / 2374.0e-12 = 1.0 / 2.374e-12 = 421.159e9 ops/Joule = OPS/s /Watt
    
    ALU = 
    """

    # normalize to GOPS/Watt
    normalization_factor = 1.0e-9

    # 8bit ALU is in the range of 100-200 gates
    exu_metrics = execute_unit('n05t', 1.0, 1, 0, 0, 1, 1000, 0, 0, 0, 0, 1000)
    #exu_metrics.report("8bit ALU")
    #alu_ppp8 = exu_metrics.iops_per_watt * normalization_factor
    alu_ppp8 = exu_metrics.energy['total']
    # 16bit ALU is in the range of 250-500 gates
    exu_metrics = execute_unit('n05t', 1.0, 2, 0, 0, 1, 1000, 0, 0, 0, 0, 1000)
    #exu_metrics.report("16bit ALU")
    #alu_ppp16 = exu_metrics.iops_per_watt * normalization_factor
    alu_ppp16 = exu_metrics.energy['total']
    # 32bit ALU is in the range of 500-1000 gates
    exu_metrics = execute_unit('n05t', 1.0, 4, 0, 0, 1, 1000, 0, 0, 0, 0, 1000)
    #exu_metrics.report("32bit ALU")
    #alu_ppp32 = exu_metrics.iops_per_watt * normalization_factor
    alu_ppp32 = exu_metrics.energy['total']

    # 8bit FPU is in the range of 200-400 gates
    exu_metrics = execute_unit('n05t', 1.0, 1, 0, 0, 0, 0, 1, 1000, 0, 0, 1000)
    #exu_metrics.report("8bit FPU")
    #fpu_ppp8 = exu_metrics.flops_per_watt * normalization_factor
    fpu_ppp8 = exu_metrics.energy['total']
    # 16bit FPU is in the range of 1000-2000 gates
    exu_metrics = execute_unit('n05t', 1.0, 2, 0, 0, 0, 0, 1, 1000, 0, 0, 1000)
    #exu_metrics.report("8bit FPU")
    #fpu_ppp16 = exu_metrics.flops_per_watt * normalization_factor
    fpu_ppp16 = exu_metrics.energy['total']
    # 32bit FPU is in the range of 10'000-20'000 gates
    exu_metrics = execute_unit('n05t', 1.0, 4, 0, 0, 0, 0, 1, 1000, 0, 0, 1000)
    exu_metrics.report("32-bit FPU")
    #fpu_ppp32 = exu_metrics.flops_per_watt * normalization_factor
    fpu_ppp32 = exu_metrics.energy['total']

    # AVX-512 style SIMD FPU is 16x the size of a 32bit FPU, and thus in the range of 160'000-320'000 gates
    exu_metrics = execute_unit('n05t', 1.0, 4, 0, 0, 0, 0, 64, 1000, 0, 0, 1000)
    exu_metrics.report("AVX-512 SIMD")
    #avx_ppp512 = exu_metrics.flops_per_watt * normalization_factor
    avx_ppp512 = exu_metrics.energy['total']

    # CPU executing a memory bound BLAS L2 matvec
    spm_metrics = spm_matvec()
    #spm = spm_metrics.flops_per_watt * normalization_factor
    spm = spm_metrics.energy['total']

    # GPU executing a memory bound BLAS L2 matvec
    gpu_metrics = gpu_matvec()
    #gpu = gpu_metrics.flops_per_watt * normalization_factor
    gpu = gpu_metrics.energy['total']


    performance_per_watt = False
    if performance_per_watt:
        data = {'sample': ["8bit ALU", "32bit ALU", "8bit FPU", "32bit FPU", "AVX-512", "Single Core", "SIMT"],
                'cost': [100, 500, 200, 10000, 160000, 1000000, 2000000],
                'density': [alu_ppp8, alu_ppp32, fpu_ppp8, fpu_ppp32, avx_ppp512, spm, gpu]}
        samples = pd.DataFrame(data)
        print(samples)

        p = samples.plot.scatter(x='cost', y='density', title='Cost vs Performance', c='DarkBlue')
        p.set_xlabel('Cost')
        p.set_xscale('log')
        p.set_ylabel('Performance (GOPS/Watt)')
    cost_vs_energy = True
    if cost_vs_energy:
        data = {'sample': ["8bit ALU", "8bit FPU", "32bit ALU", "32bit FPU", "AVX-512", "Single Core", "SIMT"],
                'cost': [100, 200, 500, 10000, 160000, 1000000, 2000000],
                'energy': [alu_ppp8, fpu_ppp8, alu_ppp32, fpu_ppp32, avx_ppp512, spm, gpu]}
        samples = pd.DataFrame(data)
        print(samples)

        p = samples.plot.scatter(x='cost', y='energy', title='Cost vs Energy', c='DarkBlue')
        p.set_xlabel('Cost')
        p.set_xscale('log')
        p.set_ylabel('Energy (pJ)')
        p.set_yscale('log')
        # add custom label to each point in scatter plot
        up = 1
        for idx, row in samples.iterrows():
            if idx == 0:
                p.annotate(row['sample'], (row['cost'], row['energy']), xytext=(-30, 5),
                           textcoords='offset points', family='sans-serif', fontsize=12)
            else:
                p.annotate(row['sample'], (row['cost'], row['energy']), xytext=(5, 0),
                            textcoords='offset points', family='sans-serif', fontsize=12)
            up = -up

    plt.show()