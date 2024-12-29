from energysim.database.exu_energy import ExecutionUnitEnergyDatabase
from energysim.models.design_category import DesignCategory
from energysim.models.exu_configuration import ExecutionUnitConfiguration
from energysim.operator.flat_matvec import flat_matvec_exu


def fireball_matvec(core_clock_in_ghz: float, word_size_in_bytes: int, rows: int, cols: int) -> None:
    db = ExecutionUnitEnergyDatabase()
    full = db.load_data('../../data/exu_energy.csv')
    exu_energies = db.lookupEnergySet('n14t', word_size_in_bytes)
    print(exu_energies)

    agus = alus = fpus = sfus = 1
    exu_config = ExecutionUnitConfiguration(
        DesignCategory.HighVolume,
        core_clock_in_ghz,
        word_size_in_bytes,
        agus,
        alus,
        fpus,
        sfus
    )
    exu_metrics = flat_matvec_exu(rows, cols, exu_energies, exu_config)
    exu_metrics.report('fireball_matvec')


if __name__ == '__main__':
    core_clock = 3.0 # GHz
    word_size = 1 # bytes
    rows = 1 # 1024*1024
    cols = 1 # 1024
    fireball_matvec(core_clock, word_size, rows, cols)


