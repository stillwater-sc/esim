from energysim.models.design_category import DesignCategory

class GraphicsProcessingUnitConfiguration:
    def __init__(self,
                 category: 'DesignCategory',
                 core_clock_ghz: float,
                 memory_clock_ghz: float,
                 word_size_in_bytes: int,
                 cache_line_size_in_bytes: int,
                 memory_burst_size_in_bytes: int,
                 memory_channels: int,
                 channel_width_in_bytes: int,
                 threads_per_block: int,
                 blocks_per_grid: int):
        # GPU attributes
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
        # kernel configuration
        self.threads_per_block: int = threads_per_block  # typically 128 or 256 as a starting point
        self.blocks_per_grid: int = blocks_per_grid


    def __repr__(self):
        return f"GraphicsProcessingUnitConfiguration(clock='{self.core_clock}'GHz', {self.memory_clock}'GHz', ...)"

    def __str__(self):
        return f"""

        GPU Configuration:
        - Cache line size:    {self.cache_line_size} bytes
        - Memory burst size:  {self.memory_burst_size} bytes
        - Word size:          {self.word_size} bytes
        - Memory channels:    {self.memory_channels}
        - Channel width:       {self.channel_width} bytes
        
        - Design Category:    {self.category}
        - Core clock:         {self.core_clock} GHz
        - Core clock cycle:   {self.clock_cycle_ns} nsec
        - Memory clock:       {self.memory_clock} GHz
        - Memory clock cycle: {self.memory_cycle_ns} nsec
        
        - Threads per block:  {self.threads_per_block}
        - Blocks per grid:    {self.blocks_per_grid}
        """
