import pandas as pd

#
# sources: Claude.ai



class StoredProgramMachineEventEnergy:
    def __init__(self, name: str):
        # defaults
        self.cache_line_size = 64

        # all energy metrics in pJ
        self.instruction = 10
        self.execute = 1  # this is a relative, consolidated energy of an average ALU operation

        self.l1_read = 16  # 2pJ/bit, 8bit word
        self.l1_write = 768  # 3pJ/bit, 32b cacheline

        self.l2_read = 768 # 1.5x L1
        self.l2_write = 1152 # 1.5x L1

        self.l3_read = 1152 # 1.5x L2
        self.l3_write = 1728 # 1.5x L2

        self.dram_read = 3840
        self.dram_write = 5120

# database of energy per event for a computational engine
class StoredProgramMachineEnergyDatabase:
    def __init__(self, data_source: str):
        """
        Initialize the database with a data source.

        :param data_source: Path to the data source
        """
        self.data_source = data_source
        self.data = None
        self.node = None
        self.cycle_time_ns = None

    def load_data(self) -> pd.DataFrame:
        """
        Load data from the specified source.

        :return: Loaded DataFrame
        """
        self.data = pd.read_csv(self.data_source)
        return self.data

    # generate will create a set of energy values that the operator models will use to calculate
    # energy consumption of the operator
    def generate(self, node: str) -> StoredProgramMachineEventEnergy:
        self.node = node

        return StoredProgramMachineEventEnergy(node)




        # self.add_8b = 0.03
        # self.add_16b = 0.05
        # self.add_32b = 0.1
        #
        # self.mul_8b = 0.2
        # self.mul_16b = 1.0  # estimated
        # self.mul_32b = 3.1
        #
        # self.add_fp8 = 0.2  # estimated
        # self.add_fp16 = 0.4
        # self.add_fp32 = 0.9
        #
        # self.mul_fp8 = 0.4 # estimated
        # self.mul_fp16 = 1.1
        # self.mul_fp32 = 3.7
        #
        # # assuming 0.2pJ per bit
        # self.register_read_8b = 1.6
        # self.register_read_16b = 3.2
        # self.register_read_32b = 6.4
        #
        # # assuming 0.3pJ per bit
        # self.register_write_8b = 2.4
        # self.register_write_16b = 4.8
        # self.register_write_32b = 9.6




        # For a typical 14nm CMOS CPU:
        # Instruction Fetch:
        #  5-10 pJ per instruction
        # Depends on cache hierarchy, fetch width
        #
        # Instruction Decode:
        #  2-5 pJ per instruction
        # Complexity varies with instruction set architecture
        #
        # Instruction Dispatch:
        #  3-7 pJ per instruction
        # Influenced by out-of-order execution complexity
        #
        # Total energy for these stages: ~10-20 pJ per instruction, with significant variation based on specific microarchitectural design.

        # For a typical 14nm CMOS register file:
        #
        # Read energy: 0.2-0.4 pJ per bit
        # Influenced by register size, typically 32-128 bits per register
        # Specific design can reduce energy to ~0.1 pJ per bit with advanced techniques
        #
        # Write energy: 0.3-0.6 pJ per bit
        # Slightly higher than read energy due to additional charging/state-setting requirements
        # Dependent on write port design, bitline capacitance, and voltage

        # For a typical 14nm CMOS L1 cache
        # Read energy: 1-3 pJ per bit
        # Write energy: 2-4 pJ per bit.
        # Energy varies with:
        #   Cache size (typically 32-64 KB)
        #   Associativity
        #   Access transistor design
        #   Bitline and wordline capacitances
        #
        # 32byte cacheline read  = 32*8*[1,1.5,2,3pJ] = 256, 384, 512, 768pJ
        # 32byte cacheline write = 32*8*[2,3,4pJ] = 512, 768, 1024pJ

        # For a DDR5 cacheline read in a 14nm CMOS system:
        #
        # Typical cacheline size: 64 bytes (512 bits)
        # Energy per DDR5 read: Approximately 10-20 picojoules (pJ) per bit
        # Total cacheline read energy: ~5-10 nanojoules (nJ)
        #
        # For a DDR5 cacheline write in a 14nm CMOS system:
        #
        # Typical cacheline size: 64 bytes (512 bits)
        # Energy per DDR5 write: Approximately 15-25 picojoules (pJ) per bit
        # Total cacheline write energy: ~8-13 nanojoules (nJ)
        #
        # The write energy is slightly higher than read energy due to:
        #  Additional signal transitions
        #  Power required to change memory state
        #  Driving write circuitry
        #  Increased signal conditioning requirements
        #
        # Factors affecting write energy include:
        #  Memory controller design
        #  Write amplifier circuits
        #  Signal integrity techniques
        #  Operating frequency
        #  Physical transmission distance

        # 32byte DDR5 read: 32*8*[10, 15, 20pJ] = 2560, 3840, 5120pJ
        # 32byte DDR5 write: 32*8*[15, 20, 25pJ] = 3840, 5120, 6400pJ

        # CPUs (14nm TSMC):
        #
        # Typical clock frequencies: 2.5 - 3.5 GHz
        # Cycle times: Approximately 0.28 to 0.4 nanoseconds (ns)
        # Specific ranges depend on performance vs. power optimization
        # High-performance cores tend to be closer to 0.28 ns
        # Power-efficient cores tend to be closer to 0.4 ns
        #
        # GPUs (14nm TSMC):
        #
        # Typical clock frequencies: 1.0 - 1.8 GHz
        # Cycle times: Approximately 0.55 to 1.0 nanoseconds (ns)
        # Lower clock speeds compared to CPUs due to more complex parallel processing architectures
        # Emphasis on throughput rather than single-thread performance
        #
        # DSPs (14nm TSMC):
        #
        # Typical clock frequencies: 1.5 - 2.5 GHz
        # Cycle times: Approximately 0.4 to 0.66 nanoseconds (ns)
        # Optimized for specific signal processing tasks
        # Cycle times can vary based on specific DSP architecture and design goals
        #
        # These figures represent typical ranges and can vary based on specific implementation,
        # target application, and design optimization strategies. The actual cycle time is influenced
        # by factors like standard cell library, logic depth, clock tree design, and specific performance requirements.

