from typing import Any
import pandas as pd
from pyparsing import Empty


#
# sources: Claude.ai



class StoredProgramMachineEventEnergy:
    def __init__(self, node: str):
        self.node = node

        # SPM attributes
        self.cache_line_size: int = 0
        self.memory_burst_size: int = 0
        self.processor_clock: float = 0.0 # GHz
        self.clock_cycle_ns: float  = 0.0  # nsec
        self.memory_clock: float = 0.0    # GHz
        self.memory_cycle_ns: float = 0.0  # nsec

        # all energy metrics in pJ
        self.instruction: int = 0
        self.fetch: int = 0
        self.decode: int = 0
        self.dispatch: int = 0

        self.execute: int = 0   # execute is a consolidated energy of an average ALU operation
        # specific ALU operations
        self.add32b: int = 0
        self.mul32b: int = 0
        self.fadd32b: int = 0
        self.fmul32b: int = 0
        self.fma32b: int = 0
        self.fdiv32b: int = 0

        self.reg_read: int = 0
        self.reg_write: int = 0

        # cache event energies
        self.l1_read:int = 0   # per average word size
        self.l1_write:int = 0  # cacheline

        self.l2_read:int = 0  # cacheline
        self.l2_write:int = 0  # cacheline

        self.l3_read:int = 0  # cacheline
        self.l3_write:int = 0  # cacheline

        self.dram_read:int = 0 # per memory burst
        self.dram_write:int = 0 # memory burst

    def __repr__(self):
        return f"StoredProgramMachineEventEnergy(node='{self.node}', cache_line_size={self.cache_line_size}, memory_burst_size={self.memory_burst_size}, processor_clock={self.processor_clock}, memory_clock={self.memory_clock}, ...)"

    def __str__(self):
        return f"""
        Node: {self.node}

        SPM Attributes:
        - Cache line size:    {self.cache_line_size} bytes
        - Memory burst size:  {self.memory_burst_size} bytes
        - Processor clock:    {self.processor_clock} GHz
        - Core Clock cycle:   {self.clock_cycle_ns} nsec
        - Memory clock:       {self.memory_clock} GHz
        - Memory Clock cycle: {self.memory_cycle_ns} nsec

        Energy Metrics (pJ):
        - Instruction: {self.instruction}
        -   fetch:      {self.fetch}
        -   decode:     {self.decode}
        -   dispatch:   {self.dispatch}
        - Execute:     {self.execute}
        -  add32b:      {self.add32b}
        -  mul32b:      {self.mul32b}
        -  fadd32b:     {self.fadd32b}
        -  fmul32b:     {self.fmul32b}
        -  fma32b:      {self.fma32b}
        -  fdiv32b:     {self.fdiv32b}
        - Reg read:    {self.reg_read}
        - Reg write:   {self.reg_write}
        - L1 read:     {self.l1_read}
        - L1 write:    {self.l1_write}
        - L2 read:     {self.l2_read}
        - L2 write:    {self.l2_write}
        - L3 read:     {self.l3_read}
        - L3 write:    {self.l3_write}
        - DRAM read:   {self.dram_read}
        - DRAM write:  {self.dram_write}
        """

# database of energy per event for a computational engine
class StoredProgramMachineEnergyDatabase:
    def __init__(self):
        self.data = None
        self.data_source = None

    def load_data(self, data_source:str) -> pd.DataFrame:
        """
        Load data from the specified source.

        :return: Loaded DataFrame
        """
        self.data = pd.read_csv(data_source, skipinitialspace=True)
        if self.data is None:
            raise FileNotFoundError

        self.data_source = data_source
        return pd.DataFrame(self.data)

    # generate will create a Stored Program Machine configuration
    # consisting of a set of energy values, architecture attributes,
    # and performance attributes.
    # Different operator models will use this configuration to calculate
    # energy consumption and performance of the operator when executing
    # on this SPM architecture
    def generate(self, process_node: str, processor_clock_ghz: float, memory_clock_ghz: float, cache_line_size_in_bytes: int) -> StoredProgramMachineEventEnergy:
        if self.data is None:
            raise Empty

        # query the database
        df = self.data.copy()
        print(df)
        print(df.index)
        print(df.columns)
        attributes = df.columns
        select_process_node = df.loc[df['node'] == process_node]
        print(select_process_node)

        #for attribute in attributes:
        #    value = select_process_node[attribute]
        #    print(value)

        spm_config = StoredProgramMachineEventEnergy(process_node)

        # defaults
        spm_config.processor_clock = processor_clock_ghz # GHz
        spm_config.memory_clock = memory_clock_ghz    # GHz
        spm_config.cache_line_size = cache_line_size_in_bytes # in bytes
        spm_config.memory_burst_size = cache_line_size_in_bytes # in bytes

        clock_cycle_ns = 1.0 / processor_clock_ghz
        spm_config.clock_cycle_ns = clock_cycle_ns
        memory_cycle_ns = 1.0 / memory_clock_ghz
        spm_config.memory_cycle_ns = memory_cycle_ns

        # all energy metrics in pJ
        fetch_energy = select_process_node['fetch'].values[0]
        decode_energy = select_process_node['decode'].values[0]
        dispatch_energy = select_process_node['dispatch'].values[0]
        instruction_energy =  fetch_energy + decode_energy + dispatch_energy
        spm_config.instruction = instruction_energy
        spm_config.fetch = fetch_energy
        spm_config.decode = decode_energy
        spm_config.dispatch = dispatch_energy

        add32b =  select_process_node['add32b'].values[0]
        mul32b =  select_process_node['mul32b'].values[0]
        fadd32b = select_process_node['fadd32b'].values[0]
        fmul32b = select_process_node['fmul32b'].values[0]
        fma32b =  select_process_node['fma32b'].values[0]
        fdiv32b = select_process_node['fdiv32b'].values[0]
        spm_config.add32b = add32b
        spm_config.mul32b = mul32b
        spm_config.fadd32b = fadd32b
        spm_config.fmul32b = fmul32b
        spm_config.fma32b = fma32b
        spm_config.fdiv32b = fdiv32b
        spm_config.execute = fma32b

        word_size_in_bits = 32
        # register events are per bit
        reg_read = select_process_node['reg_read'].values[0]
        reg_write = select_process_node['reg_write'].values[0]
        spm_config.reg_read = reg_read * word_size_in_bits
        spm_config.reg_write = reg_write * word_size_in_bits

        # l1 events are per bit
        l1_read_per_bit = select_process_node['l1_read'].values[0]
        l1_write_per_bit = select_process_node['l1_write'].values[0]

        spm_config.l1_read = word_size_in_bits * l1_read_per_bit
        spm_config.l1_write = cache_line_size_in_bytes*8 * l1_write_per_bit

        # l2 events are per bit
        l2_read_per_bit = select_process_node['l2_read'].values[0]
        l2_write_per_bit = select_process_node['l2_write'].values[0]
        spm_config.l2_read = cache_line_size_in_bytes*8 * l2_read_per_bit     #  768 # 1.5x L1
        spm_config.l2_write = cache_line_size_in_bytes*8 * l2_write_per_bit    # 1152 # 1.5x L1

        # l3 events are per bit
        l3_read_per_bit = select_process_node['l3_read'].values[0]
        l3_write_per_bit = select_process_node['l3_write'].values[0]
        spm_config.l3_read = cache_line_size_in_bytes*8 * l3_read_per_bit      # 1152 # 1.5x L2
        spm_config.l3_write = cache_line_size_in_bytes*8 * l3_write_per_bit    # 1728 # 1.5x L2

        # memory events are per bit
        mem_read_per_bit = select_process_node['mem_read'].values[0]
        mem_write_per_bit = select_process_node['mem_write'].values[0]
        spm_config.dram_read = cache_line_size_in_bytes*8 * mem_read_per_bit        # 3840
        spm_config.dram_write = cache_line_size_in_bytes*8 * mem_write_per_bit      # 5120

        return spm_config








