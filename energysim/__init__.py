# energysim/__init__.py

"""
Project-level initialization.
This file can include project-wide configurations, 
version information, and package-level imports.
"""

# Project version
__version__ = "0.1.0"

# Define what gets imported when someone does 'from energysim import *'
__all__ = ['core', 'database', 'execution', 'operator', 'linalg', 'utils']

# Import key classes or functions to make them easily accessible
#from .core.data_processor import DataProcessor
from .database.spm_energy import StoredProgramMachineEnergyDatabase
from .execution.spm import StoredProgramMachineMetrics
from .operator.matvec import flat_matrix_vector_multiply, flat_mv_spm
from .utils.logger import get_logger, LoggingContext, LoggerConfig
from .linalg.vector import Vector
from .linalg.matrix import Matrix
