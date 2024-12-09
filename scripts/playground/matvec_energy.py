from energysim import StoredProgramMachineEnergyDatabase, StoredProgramMachineMetrics, flat_mv_spm

if __name__ == '__main__':
    db = StoredProgramMachineEnergyDatabase()
    full = db.load_data('../../data/spm_energy.csv')
    spm_attributes = db.generate('n14l', 2.5, 3.2, 64)
    print(spm_attributes)
    energy = flat_mv_spm(16, 16, spm_attributes)
    energy.report()

