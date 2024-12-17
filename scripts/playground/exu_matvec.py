from energysim.database.exu_energy import ExecutionUnitEnergyDatabase
from energysim.models.design_category import DesignCategory
from energysim.models.exu_configuration import ExecutionUnitConfiguration
from energysim.operator.flat_matvec import flat_matvec_exu

if __name__ == '__main__':
    db = ExecutionUnitEnergyDatabase()
    full = db.load_data('../../data/exu_energy.csv')
    exu_energies = db.lookupEnergySet('n14t')
    print(exu_energies)
    rows = 1024*1024
    cols = 1024
    core_clock = 2.5 # GHz
    word_size = 4 # bytes
    agus = alus = fpus = sfus = 1
    exu_config = ExecutionUnitConfiguration(
        DesignCategory.HighVolume,
        core_clock,
        word_size,
        agus,
        alus,
        fpus,
        sfus
    )
    exu_metrics = flat_matvec_exu(rows, cols, exu_energies, exu_config)
    exu_metrics.report()

