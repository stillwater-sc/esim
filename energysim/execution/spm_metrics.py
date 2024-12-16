from tabulate import tabulate

from energysim.utils.scientific_format import scientific_format


class StoredProgramMachineMetrics:
    def __init__(self, name: str):
        self.name = name

        # tracking events and energy for a collection of categories
        self.keys:[] = [
            'instruction',
            'execute',
            'add',
            'mul',
            'fadd',
            'fmul',
            'fdiv',
            'fma',
            'register_read',
            'register_write',
            'l1_read',
            'l1_write',
            'l2_read',
            'l2_write',
            'l3_read',
            'l3_write',
            'dram_read',
            'dram_write',
            'compute',
            'data_movement',
            'cache_read',
            'cache_write',
            'l1',
            'l2',
            'l3',
            'cache',
            'memory',
            'total'
        ]
        self.events = dict.fromkeys(self.keys, 0)
        self.energy = dict.fromkeys(self.keys, 0.0)

        # machine attributes
        self.core_clock_ghz: float = 0
        self.memory_clock_ghz: float = 0
        self.cache_line_size: int = 0
        self.memory_burst: int = 0
        # performance metrics
        self.elapsed_time: float = 0
        self.instr_per_sec: float = 0   # instructions per second
        self.flops_per_sec: float = 0   # floating point operations per second
        self.memory_ops: int = 0
        self.memory_clock_ns: float = 0  # memory clock cycle in nano-seconds
        self.memops_per_sec: float = 0   # memory operations per second
        self.read_data: float = 0 # memory read in MB
        self.write_data: float = 0 # memory written in MB
        self.memory_read_bw: float = 0  # memory read bandwidth in GB/s
        self.memory_write_bw: float = 0  # memory write bandwidth in GB/s

    def __repr__(self):
        return f"StoredProgramMachineMetrics(name='{self.name}', ...)"

    def __str__(self):
        return f"""
        Name: {self.name}
        
        """

    def record(self, key: str, occurrences: int, occurrence_energy: float):
        if key in self.keys:
            self.events[key] = occurrences
            self.energy[key] = occurrences * occurrence_energy
        else:
            print(f'Key {key} not found.')

    def consolidate(self, target_key: str, keys: []):
        for key in keys:
            occurrences: int = self.events.get(key, 0)
            occurrence_energy: float = self.energy.get(key, 0.0)
            #print(f'target_key: {target_key}, key: {key}, occurrences: {occurrences}, energy: {occurrence_energy}')
            self.events[target_key] += occurrences
            self.energy[target_key] += occurrence_energy

    def gather(self, key: str) -> tuple[int, float]:
        occurrences = self.events.get(key, 0)
        occurrence_energy = self.energy.get(key, 0)
        return occurrences, occurrence_energy

    def occurrence(self, key: str) -> int:
        occurrences = self.events.get(key, 0)
        return occurrences

    def occurrence_energy(self, key: str) -> float:
        occurrence_energy = self.energy.get(key, 0)
        return occurrence_energy

    def report(self):
        instruction_events = self.events['instruction']
        execute_events = self.events['execute']
        register_read_events = self.events['register_read']
        register_write_events = self.events['register_write']
        compute_events = instruction_events + execute_events + register_read_events + register_write_events

        instruction_energy = self.energy['instruction']
        execute_energy = self.energy['execute']
        register_read_energy = self.energy['register_read']
        register_write_energy = self.energy['register_write']
        compute_energy = instruction_energy + execute_energy + register_read_energy + register_write_energy

        l1_read_events, l1_read_energy = self.gather('l1_read')
        l1_write_events, l1_write_energy = self.gather('l1_write')
        l1_events, l1_energy = self.gather('l1')
        l2_read_events, l2_read_energy = self.gather('l2_read')
        l2_write_events, l2_write_energy = self.gather('l2_write')
        l2_events, l2_energy = self.gather('l2')
        l3_read_events, l3_read_energy = self.gather('l3_read')
        l3_write_events, l3_write_energy = self.gather('l3_write')
        l3_events, l3_energy = self.gather('l3')
        cache_events, cache_energy = self.gather('cache')
        dram_read_events, dram_read_energy = self.gather('dram_read')
        dram_write_events, dram_write_energy = self.gather('dram_write')
        dram_events, dram_energy = self.gather('memory')
        data_movement_events, data_movement_energy = self.gather('data_movement')

        # reference
        #to, te = self.gather('total')
        total_energy = compute_energy + data_movement_energy
        #if te is not total_energy:
        #    print(f'validation failed: {total_energy} != {te}')

        print("Name: " + self.name)
        data = [["event", "Occurrences", "pJ", "%"],
                ["Total", "-", total_energy, 100.0],
                ["Compute", compute_events, compute_energy, 100 * compute_energy / total_energy],
                ["DataMovement", data_movement_events, data_movement_energy, 100 * data_movement_energy / total_energy],
                ["Compute", compute_events, compute_energy, 100 * compute_energy / total_energy],
                ["- Execute", execute_events, execute_energy, 100 * execute_energy / total_energy],
                ["- Instruction", instruction_events, instruction_energy, 100 * instruction_energy / total_energy],
                ["- Register Read", register_read_events, register_read_energy,
                 100 * register_read_energy / total_energy],
                ["- Register Write", register_write_events, register_write_energy,
                 100 * register_write_energy / total_energy],
                ["Cache", cache_events, cache_energy, 100 * cache_energy / total_energy],
                ["- L1 Cache", l1_events, l1_energy, 100 * l1_energy / total_energy],
                ["-  read", l1_read_events, l1_read_energy, 100 * l1_read_energy / total_energy],
                ["-  write", l1_write_events, l1_write_energy, 100 * l1_write_energy / total_energy],
                ["- L2 Cache", l2_events, l2_energy, 100 * l2_energy / total_energy],
                ["-  read", l2_read_events, l2_read_energy, 100 * l2_read_energy / total_energy],
                ["-  write", l2_write_events, l2_write_energy, 100 * l2_write_energy / total_energy],
                ["- L3 Cache", l3_events, l3_energy, 100 * l3_energy / total_energy],
                ["-  read", l3_read_events, l3_read_energy, 100 * l3_read_energy / total_energy],
                ["-  write", l3_write_events, l3_write_energy, 100 * l3_write_energy / total_energy],
                ["Memory", dram_events, dram_energy, 100 * dram_energy / total_energy],
                ["- read", dram_read_events, dram_read_energy, 100 * dram_read_energy / total_energy],
                ["- write", dram_write_events, dram_write_energy, 100 * dram_write_energy / total_energy]

                ]

        print(tabulate(data, headers="firstrow", floatfmt=".1f"))

        print()
        print(f'Machine Configuration')
        print(f'Cache line size : {self.cache_line_size} bytes')
        print(f'Memory burst    : {self.memory_burst} bytes')
        print(f'Core clock      : {self.core_clock_ghz} GHz')
        print(f'Memory clock    : {self.memory_clock_ghz} GHz')

        print()
        print(f'Performance summary')
        print(f'Elapsed time      : ' + scientific_format(self.elapsed_time, 'sec'))
        print(f'IPS               : ' + scientific_format(self.instr_per_sec, 'IPS'))
        print(f'FLOPS             : ' + scientific_format(self.flops_per_sec, 'FLOPS'))
        print(f'Memory ops        : ' + scientific_format(self.memory_ops, 'memory ops'))
        print(f'Memory clk        : ' + scientific_format(self.memory_clock_ns*1.0e-9, 'sec'))
        print(f'Data Size read    : ' + scientific_format(self.read_data, 'Bytes'))
        print(f'Data Size written : ' + scientific_format(self.write_data, 'Bytes'))
        print(f'Memory ops        : ' + scientific_format(self.memops_per_sec, 'MemoryOps/sec'))
        print(f'Memory Read       : ' + scientific_format(self.memory_read_bw, 'Bytes/sec'))
        print(f'Memory Write      : ' + scientific_format(self.memory_write_bw, 'Bytes/sec'))

