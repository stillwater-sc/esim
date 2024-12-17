import pandas as pd
from matplotlib import pyplot as plt

from energysim.database.gpu_energy import GraphicsProcessingUnitEnergyDatabase
from energysim.database.spm_energy import StoredProgramMachineEnergyDatabase
from energysim.models.design_category import DesignCategory
from energysim.models.gpu_configuration import GraphicsProcessingUnitConfiguration
from energysim.models.spm_configuration import StoredProgramMachineConfiguration
from energysim.operator.flat_matvec import flat_matvec_gpu, flat_matvec_spm


def randomize_spm(nr_samples: int, process_node: str):
    db = StoredProgramMachineEnergyDatabase()
    full = db.load_data('../../data/spm_energy.csv')  # this returns a full DataFrame, but we ignore it
    #print(full)
    #print(full.index)
    #print(full.columns)
    nodes = full['node']
    #print(nodes)
    locator = (full['node'] == process_node)
    selected_node = full.loc[locator]
    if selected_node is None:
        raise ValueError(f'Process {selected_node} not supported')

    # create a database of progressively more performant Stored Program Machines
    # clock frequency range of a Intel iCore 2 2018-2019 in 14nm Intel
    low_cf = 2.5 # GHz
    high_cf = 4.0 # GHz
    processor_clock_ghz = low_cf
    processor_clock_increment = (high_cf - low_cf)/nr_samples
    low_mf = 2.7 # GHz   that is a 2700MHz DDR
    high_mf = 4.5 # GHz  that is a 4500MHz DDR
    memory_clock_ghz = low_mf
    memory_clock_increment = (high_mf - low_mf)/nr_samples
    category = DesignCategory.HighVolume
    spm_configs = []
    for sample in range(nr_samples):
        spm_configs.append(StoredProgramMachineConfiguration(category, processor_clock_ghz, memory_clock_ghz, 64))
        processor_clock_ghz += processor_clock_increment
        memory_clock_ghz += memory_clock_increment

    data = {'sample': [], 'category': [], 'core_clock_ghz': [], 'memory_clock_ghz': [], 'performance': [], 'energy': []}
    df = pd.DataFrame(data)

    base_sample = db.lookupEnergySet(process_node, spm_configs[0].cache_line_size)
    proportion = 0.25
    for sample in range(nr_samples):
        sample_name = process_node + '_' + str(sample)
        spm_energies = base_sample.generate_randomized_delta(sample_name, proportion, spm_configs[sample])
        spm_metrics = flat_matvec_spm(16, 16, spm_energies, spm_configs[sample])
        #spm_metrics.report()
        processor_clock_ghz = spm_configs[sample].core_clock
        memory_clock_ghz = spm_configs[sample].memory_clock
        new_row = pd.DataFrame(
            {'sample': [sample_name],
             'category': [category],
             'core_clock_ghz': [processor_clock_ghz],
             'memory_clock_ghz': [memory_clock_ghz],
             'performance': [spm_metrics.instr_per_sec],
             'energy': [spm_metrics.occurrence_energy('total')* 1.0e-6]}  # renormalize pJ to microJ
        )
        df = pd.concat([df,new_row], ignore_index=True)

    return df


def randomize_gpu(nr_samples: int, process_node: str):
    db = GraphicsProcessingUnitEnergyDatabase()
    full = db.load_data('../../data/gpu_energy.csv')  # this returns a full DataFrame, but we ignore it
    nodes = full['node']
    #print(nodes)
    locator = (full['node'] == process_node)
    selected_node = full.loc[locator]
    if selected_node is None:
        raise ValueError(f'Process {selected_node} not supported')

    # workload attributes
    rows = 16
    cols = 16
    # Configure grid and block dimensions for a one-dimensional blocking: one thread per row-col dot product
    threads_per_block = 128
    blocks_per_grid = (rows + threads_per_block - 1) // threads_per_block
    word_size_in_bits = 32
    memory_burst_size_in_bytes = 64   # typically can be 32b, 64b, 128bytes

    # create a database of progressively more performant Graphics Processing Units
    # clock frequency range of a GeForce 10 series (Pascal) 2018-2019 in 14nm TSMC and Samsung
    low_cf = 1.0 # GHz
    high_cf = 1.5 # GHz
    core_clock_ghz = low_cf
    core_clock_increment = (high_cf-low_cf)/nr_samples
    low_mf = 3.0 # GHz
    high_mf = 4.0 # GHz
    memory_clock_ghz = low_mf
    memory_clock_increment = (high_mf - low_cf)/nr_samples
    category = DesignCategory.HighVolume
    gpu_configs = []


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
    gpus = randomize_gpu(10, 'n14t')
    print(gpus)
    p = gpus.plot.scatter(x='performance', y='energy', title='Performance vs Energy', c='DarkBlue')
    p.set_xlabel('Performance (TOPS)')
    p.set_ylabel('Energy (micro-J)')
    plt.show()
    cpus = randomize_spm(10, 'n14t')
    print(cpus)
    p = cpus.plot.scatter(x='performance', y='energy', title='Performance vs Energy', c='DarkRed')

    designs = gpus
    designs = pd.concat([designs, cpus], ignore_index=True)
    p = designs.plot.scatter(x='performance', y='energy', title='Performance vs Energy', c='DarkGreen')
    p.set_xlabel('Performance (TOPS)')
    p.set_ylabel('Energy (micro-J)')
    plt.show()

if __name__ == '__main__':
    generate_experiment()