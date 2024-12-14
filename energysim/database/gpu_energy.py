import pandas as pd

from pyparsing import Empty

from energysim.models.design_category import DesignCategory
from energysim.models.gpu_configuration import GraphicsProcessingUnitConfiguration
from energysim.utils.randomizer import randomizer


# Characteristic event energies of a Graphics Processing Unit
# organized as a Single Instruction Multiple Thread (SIMT) machine
#
class GraphicsProcessingUnitEnergy:
    def __init__(self, identifier: str):
        self.identifier = identifier

        # all energy metrics in pJ
        self.instruction: float = 0
        self.fetch: float = 0
        self.decode: float = 0
        self.dispatch: float = 0

        self.execute: float = 0  # execute is a consolidated energy of an average ALU operation
        # specific ALU operations
        self.add32b: float = 0
        self.mul32b: float = 0
        self.fadd32b: float = 0
        self.fmul32b: float = 0
        self.fma32b: float = 0
        self.fdiv32b: float = 0

        self.register_read: float = 0
        self.register_write: float = 0

        # cache event energies
        self.l1_read: float = 0  # per average word size
        self.l1_write: float = 0  # cacheline

        self.l2_read: float = 0  # cacheline
        self.l2_write: float = 0  # cacheline

        self.l3_read: float = 0  # cacheline
        self.l3_write: float = 0  # cacheline

        self.dram_read: float = 0  # per memory burst
        self.dram_write: float = 0  # memory burst

        # consolidated energies
        self.total: float = 0
        self.compute: float = 0
        self.data_movement: float = 0

    def __repr__(self):
        return f"StoredProgramMachineEnergy(node='{self.node}', cache_line_size={self.cache_line_size}, memory_burst_size={self.memory_burst_size}, processor_clock={self.processor_clock}, memory_clock={self.memory_clock}, ...)"

    def __str__(self):
        return f"""
        Node: {self.node}

        Energy Metrics (pJ):
        - Total        {self.total}
        -  compute:       {self.compute}
        -  data movement: {self.data_movement}

        - Compute
        - Instruction: {self.instruction}
        -  fetch:       {self.fetch}
        -  decode:      {self.decode}
        -  dispatch:    {self.dispatch}
        - Operand:     {self.register_read + self.register_write}
        -  Reg read:    {self.register_read}
        -  Reg write:   {self.register_write}
        - Execute:     {self.execute}
        -  add:         {self.add32b}
        -  mul:         {self.mul32b}
        -  fadd:        {self.fadd32b}
        -  fmul:        {self.fmul32b}
        -  fma:         {self.fma32b}
        -  fdiv:        {self.fdiv32b}

        - Data Movement
        -  L1 read:       {self.l1_read}
        -  L1 write:      {self.l1_write}
        -  L2 read:       {self.l2_read}
        -  L2 write:      {self.l2_write}
        -  DRAM read:     {self.dram_read}
        -  DRAM write:    {self.dram_write}
        """

    # Given an energy profile, randomize the values a little bit to emulate different designs
    # Energy efficient designs would start from the 'low' corner of the energy profiles,
    # high performance designs would start from the 'high' corner of the profile,
    # and the mid-range designs would start from the 'typical' profile
    def generate_randomized_delta(self, new_name: str, proportion: float,
                                  config: 'StoredProgramMachineConfiguration') -> 'StoredProgramMachineEnergy':

        # basic idea:
        # we are taking an energy estimate of a logic/arithmetic circuit and we are going to
        # randomize that around the value. We'll postulate that a range of (-25%, +25%)
        # is sufficiently interesting
        new_sample = StoredProgramMachineEnergy(new_name)

        if config.category == DesignCategory.EnergyEfficient:
            lowerbound = 1.0 - proportion
            upperbound = 1.0
        elif config.category == DesignCategory.HighVolume:
            lowerbound = 1.0 - (0.5 * proportion)
            upperbound = 1.0 + (0.5 * proportion)
        elif config.category == DesignCategory.HighPerformance:
            lowerbound = 1.0
            upperbound = 1.0 + proportion
        else:
            lowerbound = 0.0
            upperbound = 0.0

        # instruction energies
        new_sample.fetch = randomizer(self.fetch, lowerbound, upperbound)
        new_sample.decode = randomizer(self.decode, lowerbound, upperbound)
        new_sample.dispatch = randomizer(self.dispatch, lowerbound, upperbound)
        new_sample.instruction = self.fetch + self.decode + self.dispatch

        # execute energies
        new_sample.add32b = randomizer(self.add32b, lowerbound, upperbound)
        new_sample.mul32b = randomizer(self.mul32b, lowerbound, upperbound)
        new_sample.fadd32b = randomizer(self.fadd32b, lowerbound, upperbound)
        new_sample.fmul32b = randomizer(self.fmul32b, lowerbound, upperbound)
        new_sample.fma32b = randomizer(self.fma32b, lowerbound, upperbound)
        new_sample.fdiv32b = randomizer(self.fdiv32b, lowerbound, upperbound)
        new_sample.execute = self.fma32b  # approximate until we have instruction profiles

        new_sample.register_read = randomizer(self.register_read, lowerbound, upperbound)
        new_sample.register_write = randomizer(self.register_write, lowerbound, upperbound)

        # cache event energies
        new_sample.l1_read = randomizer(self.l1_read, lowerbound, upperbound)
        new_sample.l1_write = randomizer(self.l1_write, lowerbound, upperbound)

        new_sample.l2_read = randomizer(self.l2_read, lowerbound, upperbound)
        new_sample.l2_write = randomizer(self.l2_write, lowerbound, upperbound)

        new_sample.l3_read = randomizer(self.l3_read, lowerbound, upperbound)
        new_sample.l3_write = randomizer(self.l3_write, lowerbound, upperbound)

        new_sample.dram_read = randomizer(self.dram_read, lowerbound, upperbound)
        new_sample.dram_write = randomizer(self.dram_write, lowerbound, upperbound)

        # consolidated energies
        new_sample.compute = self.instruction + self.execute + self.register_read + self.register_write
        l1 = self.l1_read + self.l1_write
        l2 = self.l2_read + self.l2_write
        l3 = self.l3_read + self.l3_write
        memory = self.dram_read + self.dram_write
        new_sample.data_movement = l1 + l2 + l3 + memory
        new_sample.total = self.compute + self.data_movement
        return new_sample


# database of energy per event for a computational engine
class StoredProgramMachineEnergyDatabase:
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
    # and return a set of energy values for different Stored Program Machine events,
    # such as, l1 cache read, or a 32b floating-point multiplication.
    # Different operator models will use this configuration to calculate
    # energy consumption and performance of the operator when executing
    # on a SPM architecture
    def lookupEnergySet(self, node: str, cache_line_size_in_bytes: int) -> StoredProgramMachineEnergy:
        if self.data is None:
            raise Empty

        # query the database
        df = self.data.copy()
        # print(df)
        # print(df.index)
        # print(df.columns)
        process_node = df.loc[df['node'] == node]
        if process_node is None:
            raise ValueError(f'Process {process_node} not supported')

        # create the set, initialize with the node string
        spm_energies = StoredProgramMachineEnergy(node)

        # all energy metrics in pJ
        fetch_energy = process_node['fetch'].values[0]
        decode_energy = process_node['decode'].values[0]
        dispatch_energy = process_node['dispatch'].values[0]
        instruction_energy = fetch_energy + decode_energy + dispatch_energy
        spm_energies.instruction = instruction_energy
        spm_energies.fetch = fetch_energy
        spm_energies.decode = decode_energy
        spm_energies.dispatch = dispatch_energy

        add32b = process_node['add32b'].values[0]
        mul32b = process_node['mul32b'].values[0]
        fadd32b = process_node['fadd32b'].values[0]
        fmul32b = process_node['fmul32b'].values[0]
        fma32b = process_node['fma32b'].values[0]
        fdiv32b = process_node['fdiv32b'].values[0]
        spm_energies.add32b = add32b
        spm_energies.mul32b = mul32b
        spm_energies.fadd32b = fadd32b
        spm_energies.fmul32b = fmul32b
        spm_energies.fma32b = fma32b
        spm_energies.fdiv32b = fdiv32b
        spm_energies.execute = fma32b

        word_size_in_bits = 32
        # register events are per bit
        register_read = process_node['reg_read'].values[0]
        register_write = process_node['reg_write'].values[0]
        spm_energies.register_read = register_read * word_size_in_bits
        spm_energies.register_write = register_write * word_size_in_bits

        # l1 events are per bit
        l1_read_per_bit = process_node['l1_read'].values[0]
        l1_write_per_bit = process_node['l1_write'].values[0]

        spm_energies.l1_read = word_size_in_bits * l1_read_per_bit
        spm_energies.l1_write = cache_line_size_in_bytes * 8 * l1_write_per_bit

        # l2 events are per bit
        l2_read_per_bit = process_node['l2_read'].values[0]
        l2_write_per_bit = process_node['l2_write'].values[0]
        spm_energies.l2_read = cache_line_size_in_bytes * 8 * l2_read_per_bit  # 768 # 1.5x L1
        spm_energies.l2_write = cache_line_size_in_bytes * 8 * l2_write_per_bit  # 1152 # 1.5x L1

        # l3 events are per bit
        l3_read_per_bit = process_node['l3_read'].values[0]
        l3_write_per_bit = process_node['l3_write'].values[0]
        spm_energies.l3_read = cache_line_size_in_bytes * 8 * l3_read_per_bit  # 1152 # 1.5x L2
        spm_energies.l3_write = cache_line_size_in_bytes * 8 * l3_write_per_bit  # 1728 # 1.5x L2

        # memory events are per bit
        mem_read_per_bit = process_node['mem_read'].values[0]
        mem_write_per_bit = process_node['mem_write'].values[0]
        spm_energies.dram_read = cache_line_size_in_bytes * 8 * mem_read_per_bit  # 3840
        spm_energies.dram_write = cache_line_size_in_bytes * 8 * mem_write_per_bit  # 5120

        return spm_energies








