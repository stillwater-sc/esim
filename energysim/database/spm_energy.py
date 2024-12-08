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
        self.cycle_time_ns = None

    def load_data(self) -> pd.DataFrame:
        """
        Load data from the specified source.

        :return: Loaded DataFrame
        """
        self.data = pd.read_csv(self.data_source, skipinitialspace=True)
        return pd.DataFrame(self.data)

    # generate will create a set of energy values that the operator models will use to calculate
    # energy consumption of the operator
    def generate(self, node: str) -> StoredProgramMachineEventEnergy:
        # query the database
        # df = self.data.query('node == @node')
        df = pd.DataFrame(self.data)
        print(df.columns)
        n14t = (df[["n14t"]])
        print(n14t)
        return StoredProgramMachineEventEnergy(node)








