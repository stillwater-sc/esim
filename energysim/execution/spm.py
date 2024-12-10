from tabulate import tabulate

class StoredProgramMachineMetrics:
    def __init__(self, name: str):
        self.name = name
        # energy consumption variables
        self.instruction = 0
        self.execute = 0
        self.register_read = 0
        self.register_write = 0
        self.compute = 0
        self.l1_read = 0
        self.l1_write = 0
        self.l2_read = 0
        self.l2_write = 0
        self.l3_read = 0
        self.l3_write = 0
        self.dram_read = 0
        self.dram_write = 0
        # consolidate sets
        self.cache_read = 0
        self.cache_write = 0
        self.compute = 0
        self.l1 = 0
        self.l2 = 0
        self.l3 = 0
        self.cache = 0
        self.memory = 0
        self.data_movement = 0
        self.total = 0
        # performance metrics
        self.TIPS = 0   # instructions per second
        self.TOPS = 0   # floating point operations per second
        self.MemGOPS = 0   # memory operations per second


