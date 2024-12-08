import pandas as pd

from energysim.database.spm_energy import StoredProgramMachineEnergyDatabase
from energysim.operator.matvec import flat_mv_spm


def randomize_spm(samples: int):
    db = StoredProgramMachineEnergyDatabase('../../data/spm_energy.csv')
    energy_db = db.load_data()
    print(energy_db)
    df = pd.DataFrame()
    for sample in range(samples):
        energies = db.generate('n14')
        energy = flat_mv_spm(16, 16, energies)
        energy.report()

    return df


if __name__ == '__main__':
    df = randomize_spm(10)
    #df.plot.scatter(x='Performance', y='Energy (mJ)', title='Performance vs Energy', c='DarkBlue')