from energysim.database.dfa_energy import DomainFlowArchitectureEnergyDatabase
from energysim.models.design_category import DesignCategory
from energysim.models.spm_configuration import StoredProgramMachineConfiguration
from energysim.operator.flat_matvec import flat_matvec_spm, DomainFlowArchitectureConfiguration, flat_matvec_dfa

if __name__ == '__main__':
    db = DomainFlowArchitectureEnergyDatabase()
    full = db.load_data('../../data/dfa_energy.csv')
    dfa_energies = db.lookupEnergySet('n14t', 64)
    print(dfa_energies)

    rows = 1024*1024
    cols = 1024
    core_clock = 2.5 # GHz
    memory_clock = 3.2 # 3.2 GHz
    cache_line_size = 64 # bytes
    memory_burst_size = 64 # bytes
    word_size = 4 # bytes
    memory_channels = 1
    channel_width = 8 # bytes  typical DDR channel is 64bit == 8 bytes
    dfa_config = DomainFlowArchitectureConfiguration(
        DesignCategory.HighVolume,
        core_clock,
        memory_clock,
        word_size,
        cache_line_size,
        memory_burst_size,
        memory_channels,
        channel_width
    )
    dfa_metrics = flat_matvec_dfa(rows, cols, dfa_energies, dfa_config)
    dfa_metrics.report()

