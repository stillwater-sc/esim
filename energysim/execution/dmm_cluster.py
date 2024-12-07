from tabulate import tabulate


class DistributedMemoryCluster:
    def __init__(self, name: str):
        self.name = name
        self.compute = 0
        self.memory_read = 0
        self.memory_write = 0
        self.network_read = 0
        self.network_write = 0
        self.storage_read = 0
        self.storage_write = 0


    def report(self):
        print('Name: ' + self.name)
        total_compute = self.compute
        total_memory = self.memory_read + self.memory_write
        total_network = self.network_read + self.network_write
        total_storage = self.storage_read + self.storage_write
        total_energy = total_compute + total_memory + total_network + total_storage

        data = [["event", "pJ", "%"],
                ["Compute", total_compute, 100 * total_compute/total_energy],
                ["Memory", total_memory, 100 * total_memory/total_energy],
                ["Network", total_network, 100 * total_network / total_energy],
                ["Storage", total_storage, 100 * total_storage / total_energy]
                ]

        print(tabulate(data, headers="firstrow", floatfmt=".1f"))