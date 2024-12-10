# Sweep energies per operator as a function of operator size
import pandas as pd
import matplotlib.pyplot as plt

from energysim import StoredProgramMachineEnergyDatabase
from energysim.operator.matvec import flat_mv_spm


def sweep_operator_size(sizes):
    energies = []

    db = StoredProgramMachineEnergyDatabase()
    full = db.load_data('../../data/spm_energy.csv')
    spm_attributes = db.generate('n14l', 2.5, 3.2, 64)
    for size in sizes:
        energy = flat_mv_spm(size, size, spm_attributes)
        energies.append(energy.total*1e-9)

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


