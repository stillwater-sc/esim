import pandas as pd
from matplotlib import pyplot as plt

from energysim.database.spm_energy import StoredProgramMachineEnergyDatabase
from energysim.models.spm_configuration import StoredProgramMachineConfiguration
from energysim.operator.matvec import flat_mv_spm


def randomize_spm(samples: int, process_node: str):
    db = StoredProgramMachineEnergyDatabase()
    full = db.load_data('../../data/spm_energy.csv')  # this returns a full DataFrame, but we ignore it
    #print(full)
    #print(full.index)
    #print(full.columns)
    nodes = full['node']
    if process_node in nodes:
        # construct the sample regions
        low = process_node + 'l'
        high = process_node + 'h'
    else:
        raise ValueError(f'Process {process_node} not supported')

    spm_config = StoredProgramMachineConfiguration(2.5, 3.2, 64)

    data = {'sample': [], 'performance': [], 'energy': []}
    df = pd.DataFrame(data)
    for sample in range(samples):
        spm_energies = db.generate('n14l', spm_config.cache_line_size)
        spm_metrics = flat_mv_spm(16, 16, spm_energies, spm_config)
        spm_metrics.report()
        sample = process_node + str(sample)
        new_row = pd.DataFrame({'sample': [sample], 'performance': [spm_metrics.TIPS], 'energy': [spm_metrics.occurrence_energy('total')]})
        df = pd.concat([df,new_row], ignore_index=True)

    return df


if __name__ == '__main__':
    samples = randomize_spm(2, 'n14t')
    print(samples)
    samples.plot.scatter(x='performance', y='energy', title='Performance vs Energy', c='DarkBlue')
    plt.show()