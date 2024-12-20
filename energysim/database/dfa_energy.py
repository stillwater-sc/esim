import pandas as pd

class DomainFlowArchitectureEnergy:
    def __init__(self, identifier: str):
        self.identifier = identifier

        self.cam_cycle_time_ns: float

        self.istore: float = 0
        self.istore_dispatch: float = 0   # egress flow
        self.istore_operand_write: float = 0 # data token ingress flow

        self.execute: float = 0
        self.add: float = 0
        self.mul: float = 0
        self.fma: float = 0
        self.fdiv: float = 0

        self.data_token: float = 0
        self.pipe_read: float = 0
        self.pipe_write: float = 0

        # shared memory stream controller
        self.smem_streamer: float = 0
        self.str_read: float = 0
        self.str_write: float = 0
        # shared memory stream controller generates the request stream
        # from the page caches into the shared memory.

        # L1 holds the data that will get streamed into the fabric
        self.l1_read: float = 0
        self.l1_write: float = 0
        # SMEM - shared memory accesses
        self.smem_read: float = 0  # 32b word
        self.smem_write: float = 0  # 32b word

        # DMA engines will stream the blocks from local memory
        # to the shared memory L3
        self.dma: float = 0
        self.dma_read: float = 0
        self.dma_write: float = 0
        # GMEM - global memory accesses
        self.gmem_read: float = 0  # per memory burst
        self.gmem_write: float = 0  # memory burst

        # consolidated energies
        self.total: float = 0
        self.compute: float = 0
        self.data_movement: float = 0

    def __repr__(self):
        return f"DomainFlowArchitectureEnergy(identifier='{self.identifier}',...)"

    def __str__(self):
        return f"""
        ID: {self.identifier}

        Energy Metrics (pJ):
        - Compute
        - Wavefront:    {self.wavefront}
        -  instruction:  {self.instruction}
        - iStore:       {self.istore}
        -  dispatch:    {self.istore_dispatch}
        -  token write: {self.istore_operand_write}
        - Operand:      {self.reg_read + self.reg_write}
        -  Reg read:     {self.reg_read}
        -  Reg write:    {self.reg_write}
        - Execute:      {self.execute}
        -  add:          {self.add}
        -  mul:          {self.mul}
        -  fma:          {self.fma}
        -  fdiv:         {self.fdiv}

        - Data Movement
        -  L1 read:     {self.l1_read}
        -  L1 write:    {self.l1_write}
        -  smem read:   {self.smem_read}
        -  smem write:  {self.smem_write}
        -  gmem read:   {self.gmem_read}
        -  gmem write:  {self.gmem_write}
        """

# database of energy per event for a Domain Flow Architecture computational engine
class DomainFlowArchitectureEnergyDatabase:
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
    def lookupEnergySet(self, node: str) -> DomainFlowArchitectureEnergy:
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
        dfa_energies = DomainFlowArchitectureEnergy(node)

        # all energy metrics are in pJ

        istore_dispatch = process_node['itoken'].values[0]   # instruction token is an eviction from the iStore
        istore_data_token = process_node['dtoken'].values[0] # data token is an operand write into the iStore
        dfa_energies.istore_dispatch = istore_dispatch   # egress flow
        dfa_energies.istore_operand_write = istore_data_token # data token ingress flow

        self.execute: float = 0
        dfa_energies.add = process_node['add'].values[0]
        dfa_energies.mul = process_node['mul'].values[0]
        dfa_energies.fma = process_node['fma'].values[0]
        dfa_energies.fdiv = process_node['fdiv'].values[0]

        # we should only be writing: write into the pipeline register
        # that triggers the data token processing
        dfa_energies.pipe_write = process_node['pipewr'].values[0]

        # L1 holds the data that will get streamed into the fabric
        dfa_energies.l1_read = process_node['l1_read'].values[0]
        dfa_energies.l1_write = process_node['l1_write'].values[0]
        # SMEM - shared memory accesses
        dfa_energies.smem_read = process_node['smem_read'].values[0]
        dfa_energies.smem_write = process_node['smem_write'].values[0]
        # GMEM - global memory accesses
        dfa_energies.gmem_read = process_node['gmem_read'].values[0]
        dfa_energies.gmem_write = process_node['gmem_write'].values[0]

        return dfa_energies

# Typical cycle times for CAMs in 14nm TSMC process technology generally range between 0.8 to 1.5 nanoseconds (ns).
# This range can vary depending on specific design parameters such as:
#
# Memory depth and width
# Comparison circuitry complexity
# Power consumption constraints
# Specific CAM architecture (ternary, binary)
# Peripheral circuit design
#
# The lower end of the cycle time spectrum (around 0.8-1.0 ns) is typically achieved in high-performance designs
# with optimized match line sensing and precharge circuits.
#
# More complex CAM designs with additional matching flexibility might experience slightly longer
# cycle times closer to 1.5 ns.

# It's important to note that these figures are based on typical design practices and actual implementation
# can vary. For the most precise current specifications, I recommend consulting TSMC's official technology
# documentation or conducting specific characterization studies.
#
# In the cycle time range I previously mentioned (0.8 to 1.5 ns for 14nm TSMC), typical CAM sizes would be
# in the range of 1K to 16K bits. More specifically:
#
# Small CAMs: 1K-4K bits
# Medium CAMs: 8K-16K bits
# Large CAMs: 32K-64K bits
#
# The cycle times I quoted are most representative of medium-sized CAMs in the 8K to 16K bit range.
# These sizes are commonly used in applications like:
#
# Content routing in network switches
# Cache tag matching
# Address translation buffers
# Pattern matching in network processors
# Small to medium-scale associative memory lookup engines
#
# The exact size impacts cycle time through several mechanisms:
#
# Increased bit lines and word lines
# More complex match line sensing
# Additional parasitic capacitance
# Increased match logic complexity
#
# For precise cycle time and size correlations, simulation and characterization of the specific design
# would be necessary, as the relationship isn't strictly linear and depends on detailed circuit implementation.
