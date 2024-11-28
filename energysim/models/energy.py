
#
# sources
# Dally, ScaledML, 2019
# Horowitz, ISSCC, 2014

# todo: pull this from a technology file so we can assess different technologies

# database of energy per event for a computational engine
class EnergyDatabase:
    def __init__(self):
        # all energy metrics in pJ
        self.instruction = 10
        self.execute = 1  # this is a relative, consolidated energy of an average ALU operation

        self.add_8b = 0.03
        self.add_16b = 0.05
        self.add_32b = 0.1

        self.mul_8b = 0.2
        self.mul_16b = 1.0  # estimated
        self.mul_32b = 3.1

        self.add_fp8 = 0.2  # estimated
        self.add_fp16 = 0.4
        self.add_fp32 = 0.9

        self.mul_fp8 = 0.4 # estimated
        self.mul_fp16 = 1.1
        self.mul_fp32 = 3.7

        # assuming 0.2pJ per bit
        self.register_read_8b = 1.6
        self.register_read_16b = 3.2
        self.register_read_32b = 6.4

        # assuming 0.3pJ per bit
        self.register_write_8b = 2.4
        self.register_write_16b = 4.8
        self.register_write_32b = 9.6

        self.l1_read = 5 # 8KB SRAM, 32b cacheline
        self.l1_write = 8  #estimated

        self.l2_read = 10 # estimated
        self.l2_write = 15 # estimated

        self.l3_read = 25 # estimated
        self.l3_write = 40 # estimated

        self.dram_read = 640
        self.dram_write = 800


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
