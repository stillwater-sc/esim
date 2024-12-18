from tabulate import tabulate

from energysim.utils.scientific_format import scientific_format


class GraphicsProcessingUnitMetrics:
    def __init__(self, name: str):
        self.name = name

        # tracking events and energy for a collection of categories
        self.keys:[] = [
            'thread',
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
            'warp',
            'block',
            'l1_read',
            'l1_write',
            'smem_read',
            'smem_write',
            'gmem_read',
            'gmem_write',
            'compute',
            'data_movement',
            'cache_read',
            'cache_write',
            'l1',
            'smem',
            'gmem',
            'cache',
            'memory',
            'total'
        ]
        self.events = dict.fromkeys(self.keys, 0)
        self.energy = dict.fromkeys(self.keys, 0.0)

        # machine attributes
        self.core_clock_ghz: float = 0
        self.memory_clock_ghz: float = 0
        self.word_size: int = 0
        self.cache_line_size: int = 0
        self.memory_burst: int = 0
        self.memory_channels: int = 0
        self.channel_width: int = 0
        self.max_memory_bw: float = 0
        # kernel attributes
        self.threads_per_block: int = 0
        self.blocks_per_grid: int = 0
        self.nr_of_warps: int = 0
        # performance metrics
        self.elapsed_time: float = 0    # in seconds
        self.instr_per_sec: float = 0   # instructions per second
        self.flops_per_sec: float = 0   # floating point operations per second
        self.memory_transactions: int = 0
        self.memory_clock_ns: float = 0  # memory clock cycle in nano-seconds
        self.memops_per_sec: float = 0   # memory operations per second
        self.read_data: float = 0 # memory read in MB
        self.write_data: float = 0 # memory written in MB
        self.memory_read_bw: float = 0  # memory read bandwidth in GB/s
        self.memory_write_bw: float = 0  # memory write bandwidth in GB/s
        # normalized performance
        self.total_flops: float = 0
        self.power: float = 0
        self.flops_per_watt: float = 0

    def __repr__(self):
        return f"GraphicsProcessingUnitMetrics(name='{self.name}', ...)"

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
        smem_read_events, smem_read_energy = self.gather('smem_read')
        smem_write_events, smem_write_energy = self.gather('smem_write')
        smem_events, smem_energy = self.gather('smem')
        cache_events, cache_energy = self.gather('cache')
        gmem_read_events, gmem_read_energy = self.gather('gmem_read')
        gmem_write_events, gmem_write_energy = self.gather('gmem_write')
        gmem_events, gmem_energy = self.gather('memory')
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
                ["- Shared Memory", smem_events, smem_energy, 100 * smem_energy / total_energy],
                ["-  read", smem_read_events, smem_read_energy, 100 * smem_read_energy / total_energy],
                ["-  write", smem_write_events, smem_write_energy, 100 * smem_write_energy / total_energy],
                ["Global Memory", gmem_events, gmem_energy, 100 * gmem_energy / total_energy],
                ["- read", gmem_read_events, gmem_read_energy, 100 * gmem_read_energy / total_energy],
                ["- write", gmem_write_events, gmem_write_energy, 100 * gmem_write_energy / total_energy]

                ]

        print(tabulate(data, headers="firstrow", floatfmt=".1f"))

        print()
        print(f'Machine Configuration')
        print(f'Core clock          : {self.core_clock_ghz} GHz')
        print(f'Memory clock        : {self.memory_clock_ghz} GHz')
        print(f'Word size           : {self.word_size} bytes')
        print(f'Cache line size     : {self.cache_line_size} bytes')
        print(f'Memory burst        : {self.memory_burst} bytes')
        print(f'Memory channels     : {self.memory_channels}')
        print(f'Channel width       : {self.channel_width} bytes')
        print(f'Max Memory BW       : ' + scientific_format(self.max_memory_bw, "Bytes"))

        print()
        print(f'Kernel Dispatch Configuration')
        print(f'Threads per block   : {self.threads_per_block}')
        print(f'Blocks per grid     : {self.blocks_per_grid}')
        print(f'Total nr of Warps   : {self.nr_of_warps}')

        print()
        print(f'Performance summary')
        print(f'Elapsed time        : ' + scientific_format(self.elapsed_time, 'sec'))
        print(f'IPS                 : ' + scientific_format(self.instr_per_sec, 'IPS/sec'))
        print(f'FLOPS               : ' + scientific_format(self.flops_per_sec, 'FLOPS/sec'))
        print(f'Memory Transactions : ' + scientific_format(self.memory_transactions, 'Memory Transactions'))
        print(f'Memory clk          : ' + scientific_format(self.memory_clock_ns*1.0e-9, 'sec'))
        print(f'Data Size read      : ' + scientific_format(self.read_data, 'Bytes'))
        print(f'Data Size written   : ' + scientific_format(self.write_data, 'Bytes'))
        print(f'Memory Throughput   : ' + scientific_format(self.memops_per_sec, 'MemT/sec'))
        print(f'Memory Read         : ' + scientific_format(self.memory_read_bw, 'Bytes/sec'))
        print(f'Memory Write        : ' + scientific_format(self.memory_write_bw, 'Bytes/sec'))

        print()
        print(f'Normalized performance')
        print(f'Total FLOPS         : ' + scientific_format(self.total_flops, "FLOPS"))
        print(f'Power               : ' + scientific_format(self.power, "Watt"))
        print(f'FLOPS/Watt          : ' + scientific_format(self.flops_per_watt, "FLOPS/Watt"))

