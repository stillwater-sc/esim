import pandas as pd
from matplotlib import pyplot as plt

from energysim.database.spm_energy import StoredProgramMachineEnergyDatabase
from energysim.models.spm_configuration import StoredProgramMachineConfiguration, DesignCategory
from energysim.operator.flat_matvec import flat_matvec_spm


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
    processor_clock_ghz = 2.5
    processor_clock_increment = (4.0-2.5)/(nr_samples+1)
    memory_clock_ghz = 2.7
    memory_clock_increment = (6.5-2.7)/(nr_samples+1)
    category = DesignCategory.EnergyEfficient
    spm_configs = []
    midrange_index = (nr_samples // 3) - 1
    highperformance_index = (2 * nr_samples // 3)
    for sample in range(nr_samples):
        spm_configs.append(StoredProgramMachineConfiguration(category, processor_clock_ghz, memory_clock_ghz, 64))
        # calculate the new attributes for the next config
        if sample == midrange_index:
            category = DesignCategory.HighVolume
        if sample == highperformance_index:
            category = DesignCategory.HighPerformance
        processor_clock_ghz += processor_clock_increment
        memory_clock_ghz += memory_clock_increment

    data = {'sample': [], 'category': [], 'processor_core_ghz': [], 'memory_core_ghz': [], 'performance': [], 'energy': []}
    df = pd.DataFrame(data)

    base_sample = db.lookupEnergySet(process_node, spm_configs[0].cache_line_size)
    proportion = 0.25
    for sample in range(nr_samples):
        sample_name = process_node + '_' + str(sample)
        spm_energies = base_sample.generate_randomized_delta(sample_name, proportion, spm_configs[sample])
        spm_metrics = flat_matvec_spm(16, 16, spm_energies, spm_configs[sample])
        #spm_metrics.report()
        processor_clock_ghz = spm_configs[sample].processor_clock
        memory_clock_ghz = spm_configs[sample].memory_clock
        new_row = pd.DataFrame(
            {'sample': [sample_name],
             'category': [category],
             'processor_core_ghz': [processor_clock_ghz],
             'memory_core': [memory_clock_ghz],
             'performance': [spm_metrics.TIPS],
             'energy': [spm_metrics.occurrence_energy('total')* 1.0e-6]}  # renormalize pJ to microJ
        )
        df = pd.concat([df,new_row], ignore_index=True)

    return df


if __name__ == '__main__':
    samples = randomize_spm(100, 'n14t')
    print(samples)
    p = samples.plot.scatter(x='performance', y='energy', title='Performance vs Energy', c='DarkBlue')
    p.set_xlabel('Performance (TOPS)')
    p.set_ylabel('Energy (micro-J)')
    plt.show()