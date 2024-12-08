import pandas as pd
from matplotlib import pyplot as plt

from energysim.database.spm_energy import StoredProgramMachineEnergyDatabase
from energysim.operator.matvec import flat_mv_spm


def randomize_spm(samples: int, process_node: str):
    db = StoredProgramMachineEnergyDatabase('../../data/spm_energy.csv')
    db.load_data()  # this returns a full DataFrame, but we ignore it

    if process_node in ['n5', 'n7', 'n12', 'n14', 'n22', 'n28']:
        # construct the sample regions
        low = process_node + 'l'
        high = process_node + 'h'
    else:
        raise ValueError(f'Process {process_node} not supported')

    data = {'sample': [], 'performance': [], 'energy': []}
    df = pd.DataFrame(data)
    for sample in range(samples):
        energies = db.generate('n14')
        energy = flat_mv_spm(16, 16, energies)
        energy.report()
        sample = process_node + str(sample)
        new_row = pd.DataFrame({'sample': [sample], 'performance': [energy.TIPS], 'energy': [energy.total]})
        print(new_row)
        df = pd.concat([df,new_row], ignore_index=True)

    return df


if __name__ == '__main__':
    df = randomize_spm(2, 'n14')
    print(df)
    df.plot.scatter(x='performance', y='energy', title='Performance vs Energy', c='DarkBlue')
    plt.show()