from tabulate import tabulate

from energysim.utils.scientific_format import scientific_format


class ExecutionUnitMetrics:
    def __init__(self, name: str):
        self.name = name

        # tracking events and energy for a collection of categories
        self.keys: [] = [
            'agu',
            'alu',
            'fpu',
            'sfu',
            'reg_read',
            'reg_write',
            'compute',
            'data',
            'total'
        ]
        self.events = dict.fromkeys(self.keys, 0)
        self.energy = dict.fromkeys(self.keys, 0.0)

        # machine attributes
        self.core_clock_ghz: float = 0
        self.word_size: int = 0
        self.agus: int = 0
        self.alus: int = 0
        self.fpus: int = 0
        self.sfus: int = 0

        # performance metrics
        self.elapsed_time: float = 0  # in seconds
        self.agu_ops_per_sec: float = 0 # AGU operations per second
        self.alu_ops_per_sec: float = 0  # ALU operations per second
        self.fpu_ops_per_sec: float = 0  # FPU operations per second
        self.sfu_ops_per_sec: float = 0 # SFU operations per second
        self.read_data: float = 0  # data read in MB
        self.write_data: float = 0  # data written in MB
        # normalized performance
        self.total_ops: float = 0
        self.total_ops_energy: float = 0   # AGUs + ALUs energy
        self.ops_per_sec: float = 0
        # integer and address operations
        self.total_iops: float = 0
        self.total_iops_energy: float = 0   # FPUs + SFUs energy
        self.iops_per_sec: float = 0
        # floating-point operations
        self.total_flops: float = 0
        self.total_flops_energy: float = 0   # FPUs + SFUs energy
        self.flops_per_sec: float = 0

        self.power: float = 0
        self.ops_per_watt: float = 0  # all operations
        self.iops_per_watt: float = 0  # all integer operations == address and alu
        self.flops_per_watt: float = 0 # all floating-point operations == fpu and sfu

    def __repr__(self):
        return f"ExecutionUnitMetrics(name='{self.name}', ...)"

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
            # print(f'target_key: {target_key}, key: {key}, occurrences: {occurrences}, energy: {occurrence_energy}')
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
        agu_events = self.events['agu']
        alu_events = self.events['alu']
        fpu_events = self.events['fpu']
        sfu_events = self.events['sfu']
        reg_read_events = self.events['reg_read']
        reg_write_events = self.events['reg_write']
        compute_events = agu_events + alu_events + fpu_events + sfu_events
        data_events = reg_read_events + reg_write_events

        agu_energy = self.energy['agu']
        alu_energy = self.energy['alu']
        fpu_energy = self.energy['fpu']
        sfu_energy = self.energy['sfu']
        register_read_energy = self.energy['reg_read']
        register_write_energy = self.energy['reg_write']
        compute_energy = agu_energy + alu_energy + fpu_energy + sfu_energy
        data_energy = register_read_energy + register_write_energy

        # reference
        # to, te = self.gather('total')
        total_energy = compute_energy + data_energy

        print("Name: " + self.name)
        data = [["event", "Occurrences", "pJ", "%"],
                ["Total", "-", total_energy, 100.0],
                [" Compute", compute_events, compute_energy, 100 * compute_energy / total_energy],
                [" Data", data_events, data_energy, 100 * data_energy / total_energy],
                ["Compute", compute_events, compute_energy, 100 * compute_energy / total_energy],
                ["- AGU", agu_events, agu_energy, 100 * agu_energy / total_energy],
                ["- ALU", alu_events, alu_energy, 100 * alu_energy / total_energy],
                ["- FPU", fpu_events, fpu_energy, 100 * fpu_energy / total_energy],
                ["- SFU", sfu_events, sfu_energy, 100 * sfu_energy / total_energy],
                ["Data", data_events, data_energy, 100 * data_energy / total_energy],
                ["- Register Read", reg_read_events, register_read_energy, 100 * register_read_energy / total_energy],
                ["- Register Write", reg_write_events, register_write_energy, 100 * register_write_energy / total_energy],

                ]

        print(tabulate(data, headers="firstrow", floatfmt=".1f"))

        print()
        print(f'Machine Configuration')
        print(f'Core clock          : {self.core_clock_ghz} GHz')
        print(f'Word size           : {self.word_size} bytes')
        print(f'AGUs                : {self.agus}')
        print(f'ALUs                : {self.alus}')
        print(f'FPUs                : {self.fpus}')
        print(f'SFUs                : {self.sfus}')

        print()
        print()
        print(f'Performance summary')
        print(f'Elapsed time        : ' + scientific_format(self.elapsed_time, 'sec'))
        print(f'OPS                 : ' + scientific_format(self.ops_per_sec, 'OPS/sec'))
        print(f'FLOPS               : ' + scientific_format(self.flops_per_sec, 'FLOPS/sec'))
        print(f'Data Size read      : ' + scientific_format(self.read_data, 'Bytes'))
        print(f'Data Size written   : ' + scientific_format(self.write_data, 'Bytes'))

        print()
        print(f'Normalized performance')
        print(f'Power               : ' + scientific_format(self.power, "Watt"))
        print(f'Total OPS           : ' + scientific_format(self.total_ops, "OPS"))
        print(f'OPS/Watt            : ' + scientific_format(self.ops_per_watt, "OPS/Watt"))
        print(f'Total IOPS          : ' + scientific_format(self.total_iops, "IOPS"))
        print(f'IOPS/Watt           : ' + scientific_format(self.iops_per_watt, "IOPS/Watt"))
        print(f'Total FLOPS         : ' + scientific_format(self.total_flops, "FLOPS"))
        print(f'FLOPS/Watt          : ' + scientific_format(self.flops_per_watt, "FLOPS/Watt"))

