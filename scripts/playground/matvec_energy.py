from tabulate import tabulate

from energysim import StoredProgramMachineEnergyDatabase, StoredProgramMachineMetrics, flat_mv_spm
from energysim.execution.spm_events import StoredProgramMachineEvents
from energysim.models.spm_configuration import StoredProgramMachineConfiguration

if __name__ == '__main__':
    db = StoredProgramMachineEnergyDatabase()
    full = db.load_data('../../data/spm_energy.csv')
    spm_attributes = db.generate('n14l', 64)
    print(spm_attributes)
    spm_config = StoredProgramMachineConfiguration(2.5, 3.2, 64)
    spm_metrics = flat_mv_spm(16, 16, spm_attributes, spm_config)
    spm_metrics.report()

