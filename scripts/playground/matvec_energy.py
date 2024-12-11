from energysim.database.spm_energy import StoredProgramMachineEnergyDatabase
from energysim.models.spm_configuration import StoredProgramMachineConfiguration
from energysim.operator.matvec import flat_mv_spm

if __name__ == '__main__':
    db = StoredProgramMachineEnergyDatabase()
    full = db.load_data('../../data/spm_energy.csv')
    spm_energies = db.generate('n14l', 64)
    print(spm_energies)
    spm_config = StoredProgramMachineConfiguration(2.5, 3.2, 64)
    spm_metrics = flat_mv_spm(16, 16, spm_energies, spm_config)
    spm_metrics.report()

