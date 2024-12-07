# Sweep energies per operator as a function of operator size
import pandas as pd
import matplotlib.pyplot as plt

from energysim.database.energy import EnergyDatabase
from energysim.operator.matvec import flat_mv_spm


def sweep_operator_size(sizes):
    energies = []

    energydb = EnergyDatabase()
    for size in sizes:
        energy = flat_mv_spm(size, size, energydb)
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


