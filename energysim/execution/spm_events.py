

class StoredProgramMachineEvents:
    def __init__(self):
        # SPM attributes
        self.cache_line_size: int = 0
        self.memory_burst_size: int = 0
        self.processor_clock: float = 0.0 # GHz
        self.clock_cycle_ns: float  = 0.0  # nsec
        self.memory_clock: float = 0.0    # GHz
        self.memory_cycle_ns: float = 0.0  # nsec

        self.instructions: int = 0

        self.execute: int = 0   # execute is a consolidated energy of an average ALU operation
        # specific ALU occurrences
        self.add32b: int = 0
        self.mul32b: int = 0
        self.fadd32b: int = 0
        self.fmul32b: int = 0
        self.fma32b: int = 0
        self.fdiv32b: int = 0

        self.register_read: int = 0
        self.register_write: int = 0

        # cache event occurrences
        self.l1_read:int = 0   # per average word size
        self.l1_write:int = 0  # cacheline

        self.l2_read:int = 0  # cacheline
        self.l2_write:int = 0  # cacheline

        self.l3_read:int = 0  # cacheline
        self.l3_write:int = 0  # cacheline

        self.dram_read:int = 0 # per memory burst
        self.dram_write:int = 0 # memory burst

    def __repr__(self):
        return f"StoredProgramMachineEventEnergy(node='{self.node}', cache_line_size={self.cache_line_size}, memory_burst_size={self.memory_burst_size}, processor_clock={self.processor_clock}, memory_clock={self.memory_clock}, ...)"

    def __str__(self):
        return f"""
        Node: {self.node}

        SPM Attributes:
        - Cache line size:    {self.cache_line_size} bytes
        - Memory burst size:  {self.memory_burst_size} bytes
        - Processor clock:    {self.processor_clock} GHz
        - Core Clock cycle:   {self.clock_cycle_ns} nsec
        - Memory clock:       {self.memory_clock} GHz
        - Memory Clock cycle: {self.memory_cycle_ns} nsec

        Event Occurrences:
        - Instructions: {self.instructions}
        - Execute:      {self.execute}
        -  add32b:       {self.add32b}
        -  mul32b:       {self.mul32b}
        -  fadd32b:      {self.fadd32b}
        -  fmul32b:      {self.fmul32b}
        -  fma32b:       {self.fma32b}
        -  fdiv32b:      {self.fdiv32b}
        - Register File: {self.register_read + self.register_write}
        -  reg read:    {self.register_read}
        -  reg write:   {self.register_write}
        - L1 Cache     {self.l1_read + self.l1_write}
        -  read:        {self.l1_read}
        -  write:       {self.l1_write}
        - L2 Cache     {self.l2_read + self.l2_write}
        -  read:        {self.l2_read}
        -  write:       {self.l2_write}
        - L3 Cache     {self.l3_read + self.l3_write}
        -  read:        {self.l3_read}
        -  write:       {self.l3_write}
        - DRAM Memory  {self.dram_read + self.dram_write}
        -  read:        {self.dram_read}
        -  write:       {self.dram_write}
        """