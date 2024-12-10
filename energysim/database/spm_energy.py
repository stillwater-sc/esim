import pandas as pd
from pyparsing import Empty

class StoredProgramMachineEnergy:
    def __init__(self, node: str):
        self.node = node
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

        self.register_read: int = 0
        self.register_write: int = 0

        # cache event energies
        self.l1_read:int = 0   # per average word size
        self.l1_write:int = 0  # cacheline

        self.l2_read:int = 0  # cacheline
        self.l2_write:int = 0  # cacheline

        self.l3_read:int = 0  # cacheline
        self.l3_write:int = 0  # cacheline

        self.dram_read:int = 0 # per memory burst
        self.dram_write:int = 0 # memory burst

        # consolidated energies
        self.total:int = 0
        self.compute:int = 0
        self.data_movement:int = 0

    def __repr__(self):
        return f"StoredProgramMachineEventEnergy(node='{self.node}', cache_line_size={self.cache_line_size}, memory_burst_size={self.memory_burst_size}, processor_clock={self.processor_clock}, memory_clock={self.memory_clock}, ...)"

    def __str__(self):
        return f"""
        Node: {self.node}

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
        - Reg read:    {self.register_read}
        - Reg write:   {self.register_write}
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
    def generate(self, process_node: str, cache_line_size_in_bytes: int) -> StoredProgramMachineEnergy:
        if self.data is None:
            raise Empty

        # query the database
        df = self.data.copy()
        print(df)
        print(df.index)
        print(df.columns)
        select_process_node = df.loc[df['node'] == process_node]
        print(select_process_node)

        #for attribute in attributes:
        #    value = select_process_node[attribute]
        #    print(value)

        spm_energies = StoredProgramMachineEnergy(process_node)

        # all energy metrics in pJ
        fetch_energy = select_process_node['fetch'].values[0]
        decode_energy = select_process_node['decode'].values[0]
        dispatch_energy = select_process_node['dispatch'].values[0]
        instruction_energy =  fetch_energy + decode_energy + dispatch_energy
        spm_energies.instruction = instruction_energy
        spm_energies.fetch = fetch_energy
        spm_energies.decode = decode_energy
        spm_energies.dispatch = dispatch_energy

        add32b =  select_process_node['add32b'].values[0]
        mul32b =  select_process_node['mul32b'].values[0]
        fadd32b = select_process_node['fadd32b'].values[0]
        fmul32b = select_process_node['fmul32b'].values[0]
        fma32b =  select_process_node['fma32b'].values[0]
        fdiv32b = select_process_node['fdiv32b'].values[0]
        spm_energies.add32b = add32b
        spm_energies.mul32b = mul32b
        spm_energies.fadd32b = fadd32b
        spm_energies.fmul32b = fmul32b
        spm_energies.fma32b = fma32b
        spm_energies.fdiv32b = fdiv32b
        spm_energies.execute = fma32b

        word_size_in_bits = 32
        # register events are per bit
        register_read = select_process_node['reg_read'].values[0]
        register_write = select_process_node['reg_write'].values[0]
        spm_energies.register_read = register_read * word_size_in_bits
        spm_energies.register_write = register_write * word_size_in_bits

        # l1 events are per bit
        l1_read_per_bit = select_process_node['l1_read'].values[0]
        l1_write_per_bit = select_process_node['l1_write'].values[0]

        spm_energies.l1_read = word_size_in_bits * l1_read_per_bit
        spm_energies.l1_write = cache_line_size_in_bytes*8 * l1_write_per_bit

        # l2 events are per bit
        l2_read_per_bit = select_process_node['l2_read'].values[0]
        l2_write_per_bit = select_process_node['l2_write'].values[0]
        spm_energies.l2_read = cache_line_size_in_bytes*8 * l2_read_per_bit     #  768 # 1.5x L1
        spm_energies.l2_write = cache_line_size_in_bytes*8 * l2_write_per_bit    # 1152 # 1.5x L1

        # l3 events are per bit
        l3_read_per_bit = select_process_node['l3_read'].values[0]
        l3_write_per_bit = select_process_node['l3_write'].values[0]
        spm_energies.l3_read = cache_line_size_in_bytes*8 * l3_read_per_bit      # 1152 # 1.5x L2
        spm_energies.l3_write = cache_line_size_in_bytes*8 * l3_write_per_bit    # 1728 # 1.5x L2

        # memory events are per bit
        mem_read_per_bit = select_process_node['mem_read'].values[0]
        mem_write_per_bit = select_process_node['mem_write'].values[0]
        spm_energies.dram_read = cache_line_size_in_bytes*8 * mem_read_per_bit        # 3840
        spm_energies.dram_write = cache_line_size_in_bytes*8 * mem_write_per_bit      # 5120

        return spm_energies








