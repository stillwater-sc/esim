# Sweep energies per operator as a function of operator size
import pandas as pd
import matplotlib.pyplot as plt

from energysim import StoredProgramMachineEnergyDatabase
from energysim.models.spm_configuration import StoredProgramMachineConfiguration
from energysim.operator.matvec import flat_mv_spm


def sweep_operator_size(sizes):
    energies = []

    db = StoredProgramMachineEnergyDatabase()
    full = db.load_data('../../data/spm_energy.csv')
    spm_energies = db.lookupEnergySet('n14l', 64)
    spm_config = StoredProgramMachineConfiguration(2.5, 3.2, 64)
    for size in sizes:
        metrics = flat_mv_spm(size, size, spm_energies, spm_config)
        energies.append(metrics.gather('total')[1]*1e-9)

    data = {'Size': sizes, 'Energy (mJ)': energies}
    df = pd.DataFrame(data)
    return df



if __name__ == '__main__':
    # create the sweep sizes
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    df = sweep_operator_size(sizes)
    print(df)
    df.plot(x='Size', y='Energy (mJ)', title='Flat Matvec Energy (mJ)', kind='line')
    plt.show()


