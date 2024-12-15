import pandas as pd
from matplotlib import pyplot as plt

from energysim.database.gpu_energy import GraphicsProcessingUnitEnergyDatabase
from energysim.execution.gpu_metrics import GraphicsProcessingUnitMetrics
from energysim.models.gpu_configuration import GraphicsProcessingUnitConfiguration
from energysim.models.design_category import DesignCategory
from energysim.operator.flat_matvec import flat_matvec_gpu


def sample_gpu(process_node: str, category: 'DesignCategory', core_clock_ghz: float, memory_clock_ghz: float, word_size_in_bits: int, memory_burst_in_bytes: int,threads_per_block: int, blocks_per_grid: int) -> 'GraphicsProcessingUnitMetrics':
    db = GraphicsProcessingUnitEnergyDatabase()
    full = db.load_data('../../data/gpu_energy.csv')  # this returns a full DataFrame, but we ignore it
    #print(full)
    #print(full.index)
    #print(full.columns)
    nodes = full['node']
    #print(nodes)
    locator = (full['node'] == process_node)
    selected_node = full.loc[locator]
    if selected_node is None:
        raise ValueError(f'Process {selected_node} not supported')

    sample_name = process_node + '_sample'
    config = GraphicsProcessingUnitConfiguration(
        category,
        core_clock_ghz,
        memory_clock_ghz,
        word_size_in_bits,
        memory_burst_in_bytes,
        threads_per_block,
        blocks_per_grid
    )
    base_sample = db.lookupEnergySet(process_node, config.word_size)
    rows = 16
    cols = 16
    gpu_metrics = flat_matvec_gpu(rows, cols, base_sample, config)
    return gpu_metrics

def randomize_gpu(nr_samples: int, process_node: str):
    db = GraphicsProcessingUnitEnergyDatabase()
    full = db.load_data('../../data/gpu_energy.csv')  # this returns a full DataFrame, but we ignore it
    #print(full)
    #print(full.index)
    #print(full.columns)
    nodes = full['node']
    #print(nodes)
    locator = (full['node'] == process_node)
    selected_node = full.loc[locator]
    if selected_node is None:
        raise ValueError(f'Process {selected_node} not supported')

    # workload attributes
    rows = 16
    cols = 16
    # create a database of progressively more performant Graphics Processing Units
    # clock frequency range of a GeForce 10 series (Pascal) 2018-2019 in 14nm TSMC and Samsung
    low_cf = 1.0 # GHz
    high_cf = 1.5 # GHz
    core_clock_ghz = low_cf
    core_clock_increment = (high_cf-low_cf)/nr_samples
    low_mf = 3.0 # GHz
    high_mf = 6.0 # GHz
    memory_clock_ghz = low_mf
    memory_clock_increment = (high_mf - low_cf)/nr_samples
    category = DesignCategory.EnergyEfficient
    gpu_configs = []
    midrange_index = (nr_samples // 3) - 1
    highperformance_index = (2 * nr_samples // 3)
    word_size_in_bits = 32
    memory_burst_size_in_bytes = 64   # typically can be 32b, 64b, 128bytes
    # Configure grid and block dimensions for a one-dimensional blocking: one thread per row-col dot product
    threads_per_block = 128
    blocks_per_grid = (rows + threads_per_block - 1) // threads_per_block
    for sample in range(nr_samples):
        config = GraphicsProcessingUnitConfiguration(
            category,
            core_clock_ghz,
            memory_clock_ghz,
            word_size_in_bits,
            memory_burst_size_in_bytes,
            threads_per_block,
            blocks_per_grid
        )
        gpu_configs.append(config)
        # calculate the new attributes for the next config
        if sample == midrange_index:
            category = DesignCategory.HighVolume
        if sample == highperformance_index:
            category = DesignCategory.HighPerformance
        core_clock_ghz += core_clock_increment
        memory_clock_ghz += memory_clock_increment

    data = {'sample': [], 'category': [], 'core_clock_ghz': [], 'memory_clock_ghz': [], 'performance': [], 'energy': []}
    df = pd.DataFrame(data)
    base_sample = db.lookupEnergySet(process_node, gpu_configs[0].word_size)
    proportion = 0.25
    for sample in range(nr_samples):
        sample_name = process_node + '_' + str(sample)
        gpu_energies = base_sample.generate_randomized_delta(sample_name, proportion, gpu_configs[sample])
        gpu_metrics = flat_matvec_gpu(rows, cols, gpu_energies, gpu_configs[sample])
        #gpu_metrics.report()
        core_clock_ghz = gpu_configs[sample].core_clock
        memory_clock_ghz = gpu_configs[sample].memory_clock
        new_row = pd.DataFrame(
            {'sample': [sample_name],
             'category': [category],
             'core_clock_ghz': [core_clock_ghz],
             'memory_clock_ghz': [memory_clock_ghz],
             'performance': [gpu_metrics.TIPS],
             'energy': [gpu_metrics.occurrence_energy('total')* 1.0e-6]}  # renormalize pJ to microJ
        )
        df = pd.concat([df,new_row], ignore_index=True)

    return df

def generate_experiment():
    samples = randomize_gpu(100, 'n14t')
    print(samples)
    p = samples.plot.scatter(x='performance', y='energy', title='Performance vs Energy', c='DarkBlue')
    p.set_xlabel('Performance (TOPS)')
    p.set_ylabel('Energy (micro-J)')
    plt.show()

if __name__ == '__main__':
    generate_experiment()


