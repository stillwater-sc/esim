from energysim.models.design_category import DesignCategory


class DataFlowArchitectureConfiguration:
    def __init__(self,
                 category: 'DesignCategory',
                 core_clock_ghz: float,
                 memory_clock_ghz: float,
                 word_size_in_bytes: int,
                 cache_line_size_in_bytes: int,
                 memory_burst_size_in_bytes: int,
                 memory_channels: int,
                 channel_width_in_bytes: int):
        # SPM attributes
        # structure
        self.word_size: int = word_size_in_bytes
        self.cache_line_size: int = cache_line_size_in_bytes
        self.memory_burst_size: int = memory_burst_size_in_bytes
        self.memory_channels: int = memory_channels
        self.channel_width: int = channel_width_in_bytes
        # attributes
        self.category: DesignCategory = category
        self.core_clock: float = core_clock_ghz # GHz
        self.clock_cycle_ns: float  = 1.0 / core_clock_ghz  # nsec
        self.memory_clock: float = memory_clock_ghz    # GHz
        self.memory_cycle_ns: float = 1.0 / memory_clock_ghz  # nsec

    def __repr__(self):
        return f"StoredProgramMachineConfiguration(clock='{self.core_clock}'GHz', ...)"

    def __str__(self):
        return f"""

        SPM Configuration:
        - Cache line size:    {self.cache_line_size} bytes
        - Memory burst size:  {self.memory_burst_size} bytes
        - Word size:          {self.word_size} bytes

        - Design Category:    {self.category}
        - Processor clock:    {self.core_clock} GHz
        - Core Clock cycle:   {self.clock_cycle_ns} nsec
        - Memory clock:       {self.memory_clock} GHz
        - Memory Clock cycle: {self.memory_cycle_ns} nsec
        """