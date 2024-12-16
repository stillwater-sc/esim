from energysim.database.spm_energy import StoredProgramMachineEnergyDatabase
from energysim.models.design_category import DesignCategory
from energysim.models.spm_configuration import StoredProgramMachineConfiguration
from energysim.operator.flat_matvec import flat_matvec_spm

if __name__ == '__main__':
    db = StoredProgramMachineEnergyDatabase()
    full = db.load_data('../../data/spm_energy.csv')
    spm_energies = db.lookupEnergySet('n14l', 64)
    print(spm_energies)
    rows = 1024*1024
    cols = 1024
    spm_config = StoredProgramMachineConfiguration(DesignCategory.HighVolume,2.5, 3.2, 64, 64, 4)
    spm_metrics = flat_matvec_spm(rows, cols, spm_energies, spm_config)
    spm_metrics.report()

