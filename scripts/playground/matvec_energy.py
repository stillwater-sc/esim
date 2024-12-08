from energysim import StoredProgramMachineEnergyDatabase, StoredProgramMachineEnergy, flat_mv_spm

if __name__ == '__main__':
    db = StoredProgramMachineEnergyDatabase('../../data/spm_energy.csv')
    energies = db.generate('n14')
    energy = flat_mv_spm(16, 16, energies)
    energy.report()

