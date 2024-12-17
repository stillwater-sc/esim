import pandas as pd

from energysim.models.design_category import DesignCategory
from energysim.models.gpu_configuration import GraphicsProcessingUnitConfiguration
from energysim.utils.randomizer import randomizer

"""
Execute Unit Energy
"""

# Characteristic event energies for the execute stage of a processing pipeline
# assumption is that the 'core' received instruction packets that get
# routed to the respective ALU for that instruction
#   AGU    address generation units
#   ALU    integer arithmetic and logic unit
#   FPU    floating point arithmetic unit
#   SFU    special function unit, typically for reciprocal, square root, and other higher level functions
class ExecutionUnitEnergy:
    def __init__(self, identifier: str):
        self.identifier = identifier

        # all energies are in pJ
        self.agu: float = 0
        self.alu: float = 0
        self.fpu: float = 0
        self.sfu: float = 0
        self.reg_read: float = 0
        self.reg_write: float = 0

    def __repr__(self):
        return f"ExecutionUnitEnergy(identifier='{self.identifier}',...)"

    def __str__(self):
        return f"""
        ID: {self.identifier}
        
        Energy Metrics (pJ):
        - Execute Units:
        -  AGU:            {self.agu}
        -  ALU:            {self.alu}
        -  FPU:            {self.fpu}
        -  SFU:            {self.sfu}
        - Register file:
        -  Read:           {self.reg_read}
        -  Write:          {self.reg_write}
        """




# database of energy per event for a Execute Unit computational engine
class ExecutionUnitEnergyDatabase:
    def __init__(self):
        self.data = None
        self.data_source = None

    def load_data(self, data_source: str) -> pd.DataFrame:
        """
        Load data from the specified source.

        :return: Loaded DataFrame
        """
        self.data = pd.read_csv(data_source, skipinitialspace=True)
        if self.data is None:
            raise FileNotFoundError

        self.data_source = data_source
        return pd.DataFrame(self.data)

    # lookupEnergySet takes an ASIC manufacturing node name, such as, 'n14s' for 14nm slow
    # and return a set of energy values for different GPU events,
    # such as, l1 cache read, shared memory access, or a 32b floating-point multiplication.
    # Different operator models will use this configuration to calculate
    # energy consumption and performance of the operator when executing
    # on a SPM architecture
    def lookupEnergySet(self, node: str) -> ExecutionUnitEnergy:
        if self.data is None:
            raise ValueError(f'Energy Database not loaded: did you for get to call load_data(csv-file-with-energy-event-data')

        # query the database
        df = self.data.copy()  # do we need to copy it? are all the operators on the db read-only?
        # print(df)
        # print(df.index)
        # print(df.columns)
        process_node = df.loc[df['node'] == node]
        if process_node is None:
            raise ValueError(f'Process {process_node} not supported')

        # create the set, initialize with the node string
        exu_energies = ExecutionUnitEnergy(node)

        # all energy metrics in pJ

        # The instruction stream on a GPU is fetch and decode once, and
        # dispatch to Arithmetic Instruction Units inside the Streaming Multiprocessors.
        # The execute stage inside the Streaming Processor will read from the local thread register file.
        agu_energy = process_node['agu'].values[0]
        alu_energy = process_node['alu'].values[0]
        fpu_energy = process_node['fpu'].values[0]
        sfu_energy = process_node['sfu'].values[0]
        exu_energies.agu = agu_energy
        exu_energies.alu = alu_energy
        exu_energies.fpu = fpu_energy
        exu_energies.sfu = sfu_energy

        word_size_in_bits = 32
        # register events are per bit
        reg_read = process_node['reg_read'].values[0]
        reg_write = process_node['reg_write'].values[0]
        exu_energies.reg_read = reg_read * word_size_in_bits
        exu_energies.reg_write = reg_write * word_size_in_bits

        return exu_energies
