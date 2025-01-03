import pandas as pd

from energysim.models.design_category import DesignCategory
from energysim.models.gpu_configuration import GraphicsProcessingUnitConfiguration
from energysim.utils.randomizer import randomizer


# Characteristic event energies of a Graphics Processing Unit
# organized as a Single Instruction Multiple Thread (SIMT) machine
class GraphicsProcessingUnitEnergy:
    def __init__(self, identifier: str):
        self.identifier = identifier

        # all energy metrics in pJ
        self.thread: float = 0
        self.instruction: float = 0
        self.fetch: float = 0
        self.decode: float = 0
        self.dispatch: float = 0  # database is per thread, energy measured per warp (== 32 threads)

        self.execute: float = 0  # execute is a consolidated energy of an average ALU operation
        # specific ALU operations
        self.add32b: float = 0
        self.mul32b: float = 0
        self.fadd32b: float = 0
        self.fmul32b: float = 0
        self.fma32b: float = 0
        self.fdiv32b: float = 0

        self.reg_read: float = 0
        self.reg_write: float = 0

        # structural aggregations to support SIMT thread management
        self.warp: float = 0
        self.block: float = 0

        # cache event energies
        self.l1_read: float = 0  # per average word size
        self.l1_write: float = 0  # cacheline
        # SMEM - shared memory accesses
        self.smem_read: float = 0  # 32b word
        self.smem_write: float = 0  # 32b word
        # GMEM - global memory accesses
        self.gmem_read: float = 0  # per memory burst
        self.gmem_write: float = 0  # memory burst

        # consolidated energies
        self.total: float = 0
        self.compute: float = 0
        self.data_movement: float = 0

    def __repr__(self):
        return f"GraphicsProcessingUnitEnergy(identifier='{self.identifier}',...)"

    def __str__(self):
        return f"""
        ID: {self.identifier}

        Energy Metrics (pJ):
        - Compute
        - Thread:      {self.thread}
        -  instruction: {self.instruction}
        -   fetch:       {self.fetch}
        -   decode:      {self.decode}
        - Operand:     {self.reg_read + self.reg_write}
        -  Reg read:    {self.reg_read}
        -  Reg write:   {self.reg_write}
        - Execute:     {self.execute}
        -  add:         {self.add32b}
        -  mul:         {self.mul32b}
        -  fadd:        {self.fadd32b}
        -  fmul:        {self.fmul32b}
        -  fma:         {self.fma32b}
        -  fdiv:        {self.fdiv32b}
        - Warp:        {self.warp}
        -  dispatch:    {self.dispatch}
        - Data Movement
        -  L1 read:     {self.l1_read}
        -  L1 write:    {self.l1_write}
        -  smem read:   {self.smem_read}
        -  smem write:  {self.smem_write}
        -  gmem read:   {self.gmem_read}
        -  gmem write:  {self.gmem_write}
        """

    # Given an energy profile, randomize the values a little bit to emulate different designs
    # Energy efficient designs would start from the 'low' corner of the energy profiles,
    # high performance designs would start from the 'high' corner of the profile,
    # and the mid-range designs would start from the 'typical' profile
    def generate_randomized_delta(self, new_name: str, proportion: float,
                                  config: 'GraphicsProcessingUnitConfiguration') -> 'GraphicsProcessingUnitEnergy':

        # basic idea:
        # we are taking an energy estimate of a logic/arithmetic circuit and we are going to
        # randomize that around the value. We'll postulate that a range of (-25%, +25%)
        # is sufficiently interesting
        new_sample = GraphicsProcessingUnitEnergy(new_name)

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

        new_sample.reg_read = randomizer(self.reg_read, lowerbound, upperbound)
        new_sample.reg_write = randomizer(self.reg_write, lowerbound, upperbound)

        # cache event energies
        new_sample.l1_read = randomizer(self.l1_read, lowerbound, upperbound)
        new_sample.l1_write = randomizer(self.l1_write, lowerbound, upperbound)

        new_sample.smem_read = randomizer(self.smem_read, lowerbound, upperbound)
        new_sample.smem_write = randomizer(self.smem_write, lowerbound, upperbound)

        new_sample.gmem_read = randomizer(self.gmem_read, lowerbound, upperbound)
        new_sample.gmem_write = randomizer(self.gmem_write, lowerbound, upperbound)

        return new_sample


# database of energy per event for a Graphics Processing Unit computational engine
class GraphicsProcessingUnitEnergyDatabase:
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
    def lookupEnergySet(self, node: str, cache_line_size_in_bytes: int) -> GraphicsProcessingUnitEnergy:
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
        gpu_energies = GraphicsProcessingUnitEnergy(node)

        # all energy metrics in pJ

        # The instruction stream on a GPU is fetch and decode once, and
        # dispatch to Arithmetic Instruction Units inside the Streaming Multiprocessors.
        # The execute stage inside the Streaming Processor will read from the local thread register file.
        fetch_energy = process_node['fetch'].values[0]
        decode_energy = process_node['decode'].values[0]
        dispatch_energy = process_node['dispatch'].values[0]
        instruction_energy = fetch_energy + decode_energy
        gpu_energies.instruction = instruction_energy
        gpu_energies.fetch = fetch_energy
        gpu_energies.decode = decode_energy
        gpu_energies.dispatch = dispatch_energy
        thread_energy = instruction_energy + dispatch_energy * 32
        gpu_energies.thread = thread_energy

        # a

        # NVIDIA uses Warps, and AMD uses Workgroups

        # an NVIDIA SM and an AMD CU execute 4 Warps/Wavefront concurrently
        # typically scheduled one clock after each other.

        # to know how much energy is being spent by the SM/CU we need to
        # know how many Warp/Wavefronts the workload contains
        # a Warp is 32 threads, but a Wavefront is 64 work-items
        # Let's standardize on 32 threads/work-items
        # For matvec, each thread

        add32b = process_node['add32b'].values[0]
        mul32b = process_node['mul32b'].values[0]
        fadd32b = process_node['fadd32b'].values[0]
        fmul32b = process_node['fmul32b'].values[0]
        fma32b = process_node['fma32b'].values[0]
        fdiv32b = process_node['fdiv32b'].values[0]
        gpu_energies.add32b = add32b
        gpu_energies.mul32b = mul32b
        gpu_energies.fadd32b = fadd32b
        gpu_energies.fmul32b = fmul32b
        gpu_energies.fma32b = fma32b
        gpu_energies.fdiv32b = fdiv32b
        gpu_energies.execute = fma32b   # representing the average case of a collection of ALU instructions
        # for BLAS operators, they are all FMAs so reasonable assumption

        word_size_in_bits = 32
        # register events are per bit
        register_read = process_node['reg_read'].values[0]
        register_write = process_node['reg_write'].values[0]
        gpu_energies.reg_read = register_read * word_size_in_bits
        gpu_energies.reg_write = register_write * word_size_in_bits

        # l1 events are per bit
        l1_read_per_bit = process_node['l1_read'].values[0]
        l1_write_per_bit = process_node['l1_write'].values[0]

        gpu_energies.l1_read = word_size_in_bits * l1_read_per_bit
        gpu_energies.l1_write = cache_line_size_in_bytes * 8 * l1_write_per_bit

        # shared memory events are per bit
        smem_read_per_bit = process_node['smem_read'].values[0]
        smem_write_per_bit = process_node['smem_write'].values[0]
        gpu_energies.smem_read = word_size_in_bits * smem_read_per_bit
        gpu_energies.smem_write = word_size_in_bits * smem_write_per_bit

        # global memory events are per bit
        mem_read_per_bit = process_node['gmem_read'].values[0]
        mem_write_per_bit = process_node['gmem_write'].values[0]
        memory_burst_in_bytes = 64
        gpu_energies.gmem_read = memory_burst_in_bytes * 8 * mem_read_per_bit  # 3840
        gpu_energies.gmem_write = memory_burst_in_bytes * 8 * mem_write_per_bit  # 5120

        return gpu_energies








