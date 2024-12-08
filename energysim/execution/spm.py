from tabulate import tabulate

class StoredProgramMachineEnergy:
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
        self.memory_read = 0
        self.memory_write = 0
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

    def report(self):
        total_compute = self.instruction + self.execute + self.register_read + self.register_write
        self.compute = total_compute

        # data movement energy costs
        total_l1 = self.l1_read + self.l1_write
        total_l2 = self.l2_read + self.l2_write
        total_l3 = self.l3_read + self.l3_write
        total_cache = total_l1 + total_l2 + total_l3
        total_memory = self.memory_read + self.memory_write
        total_data_movement = total_cache + total_memory
        total_energy = total_compute + total_data_movement

        self.l1 = total_l1
        self.l2 = total_l2
        self.l3 = total_l3
        self.cache = total_cache
        self.memory = total_memory
        self.data_movement = total_data_movement
        self.total = total_energy

        if total_data_movement > 0:
            l1_read_relative = self.l1_read / total_data_movement
            l2_read_relative = self.l2_read / total_data_movement
            l3_read_relative = self.l3_read / total_data_movement
            memory_read_relative = self.memory_read / total_data_movement
            l1_write_relative = self.l1_write / total_data_movement
            l2_write_relative = self.l2_write / total_data_movement
            l3_write_relative = self.l3_write / total_data_movement
            memory_write_relative = self.memory_write / total_data_movement
        else:
            l1_read_relative = 0
            l2_read_relative = 0
            l3_read_relative = 0
            memory_read_relative = 0
            l1_write_relative = 0
            l2_write_relative = 0
            l3_write_relative = 0
            memory_write_relative = 0

        print("Name: " + self.name)
        data = [["event", "pJ", "%"],
                ["Total",          self.total,100.0],
                ["Compute",        self.compute,        100 * self.compute / total_energy],
                ["DataMovement",   self.data_movement,  100 * self.data_movement / total_energy],
                ["Compute",        self.compute,        100 * self.compute / total_energy],
                ["- Execute",        self.execute,        100 * self.execute / total_energy],
                ["- Instruction",    self.instruction,    100 * self.instruction/total_energy],
                ["- Register Read",  self.register_read,  100 * self.register_read/total_energy],
                ["- Register Write", self.register_write, 100 * self.register_write/total_energy],
                ["Cache",          self.cache,          100 * self.cache / total_energy],
                ["- L1 Cache",      self.l1,              100 * self.l1 / total_energy],
                ["-  L1Read",         self.l1_read,        100 * self.l1_read/total_energy],
                ["-  L1Write",        self.l1_write,       100 * self.l1_write/total_energy],
                ["- L2 Cache",      self.l2,              100 * self.l2 / total_energy],
                ["-  L2Read",         self.l2_read,        100 * self.l2_read/total_energy],
                ["-  L2Write",        self.l2_write,       100 * self.l2_write/total_energy],
                ["- L3 Cache",      self.l3,              100 * self.l3 / total_energy],
                ["-  L3Read",         self.l3_read,        100 * self.l3_read/total_energy],
                ["-  L3Write",        self.l3_write,       100 * self.l3_write/total_energy],
                ["Memory",         self.memory,         100 * self.memory / total_energy],
                ["- MemoryRead",     self.memory_read,    100 * self.memory_read/total_energy],
                ["- MemoryWrite",    self.memory_write,   100 * self.memory_write/total_energy]

                ]

        print(tabulate(data, headers="firstrow", floatfmt=".1f"))
