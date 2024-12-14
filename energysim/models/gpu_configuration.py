from energysim.models.design_category import DesignCategory

class GraphicsProcessingUnitConfiguration:
    def __init__(self, category: 'DesignCategory', processor_clock_ghz: float, memory_clock_ghz: float, cache_line_size_in_bytes: int):
        # GPU attributes
        # structure
        self.cache_line_size: int = cache_line_size_in_bytes
        self.memory_burst_size: int = cache_line_size_in_bytes
        # attributes
        self.category: DesignCategory = category
        self.processor_clock: float = processor_clock_ghz # GHz
        self.clock_cycle_ns: float  = 1.0 / processor_clock_ghz  # nsec
        self.memory_clock: float = memory_clock_ghz    # GHz
        self.memory_cycle_ns: float = 1.0 / memory_clock_ghz  # nsec


    def __repr__(self):
        return f"GraphicsProcessingUnitConfiguration(clock='{self.processor_clock}'GHz', ...)"

    def __str__(self):
        return f"""

        GPU Configuration:
        - Cache line size:    {self.cache_line_size} bytes
        - Memory burst size:  {self.memory_burst_size} bytes
        
        - Design Category:    {self.category}
        - Processor clock:    {self.processor_clock} GHz
        - Core Clock cycle:   {self.clock_cycle_ns} nsec
        - Memory clock:       {self.memory_clock} GHz
        - Memory Clock cycle: {self.memory_cycle_ns} nsec
        """
