from energysim import EnergyDatabase, StoredProgramMachineEnergy, flat_mv_spm

if __name__ == '__main__':
    energies = EnergyDatabase()
    energy = flat_mv_spm(16, 16, energies)
    energy.report()

