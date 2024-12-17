from energysim.models.design_category import DesignCategory

class ExecutionUnitConfiguration:
    def __init__(self,
                 category: 'DesignCategory',
                 core_clock_ghz: float,
                 word_size_in_bytes: int,
                 agus: int,
                 alus: int,
                 fpus: int,
                 sfus: int):
        # EXU attributes
        # structure
        self.word_size: int = word_size_in_bytes
        self.agus: int = agus
        self.alus: int = alus
        self.fpus: int = fpus
        self.sfus: int = sfus
        # attributes
        self.category: DesignCategory = category
        self.core_clock: float = core_clock_ghz # GHz
        self.clock_cycle_ns: float  = 1.0 / core_clock_ghz  # nsec


    def __repr__(self):
        return f"ExecutionUnitConfiguration(clock='{self.core_clock}'GHz', ...)"

    def __str__(self):
        return f"""

        EXU Configuration:
        - Design Category:    {self.category}
        - Core clock:         {self.core_clock} GHz
        - Core Clock cycle:   {self.clock_cycle_ns} nsec
        - Word size:          {self.word_size} bytes
        - AGU units:          {self.agus}
        - ALU units:          {self.alus}
        - FPU units:          {self.fpus}
        - SFU units:          {self.sfus}
        """
