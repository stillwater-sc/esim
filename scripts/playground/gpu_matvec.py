from energysim.database.gpu_energy import GraphicsProcessingUnitEnergyDatabase
from energysim.execution.gpu_metrics import GraphicsProcessingUnitMetrics
from energysim.models.gpu_configuration import GraphicsProcessingUnitConfiguration
from energysim.models.design_category import DesignCategory
from energysim.operator.flat_matvec import flat_matvec_gpu


def sample_gpu(process_node: str, config: 'GraphicsProcessingUnitConfiguration') -> 'GraphicsProcessingUnitMetrics':
    db = GraphicsProcessingUnitEnergyDatabase()
    full = db.load_data('../../data/gpu_energy.csv')  # this returns a full DataFrame, but we ignore it
    #print(full)
    #print(full.index)
    #print(full.columns)
    nodes = full['node']
    #print(nodes)
    locator = (full['node'] == process_node)
    selected_node = full.loc[locator]
    if selected_node is None:
        raise ValueError(f'Process {selected_node} not supported')

    sample_name = process_node + '_sample'

    base_sample = db.lookupEnergySet(process_node, config.word_size)
    print(base_sample)
    rows = 16
    cols = 16
    gpu_metrics = flat_matvec_gpu(rows, cols, base_sample, config)
    return gpu_metrics

if __name__ == '__main__':
    rows = 16
    cols = 16
    total = rows * cols
    threads_per_block = 128  # threads_per_block
    blocks_per_grid = (rows + threads_per_block - 1) // threads_per_block  # blocks_per_grid
    category = DesignCategory.HighVolume
    core_clock_ghz = 2.0
    memory_clock_ghz = 4.0
    word_size_in_bits = 32
    memory_burst_in_bytes = 64


    config = GraphicsProcessingUnitConfiguration(
        category,
        core_clock_ghz,
        memory_clock_ghz,
        word_size_in_bits,
        memory_burst_in_bytes,
        threads_per_block,
        blocks_per_grid
    )
    metrics = sample_gpu('n14t', config)
    metrics.report()
