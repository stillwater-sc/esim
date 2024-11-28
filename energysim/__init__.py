# energysim/__init__.py

"""
Project-level initialization.
This file can include project-wide configurations, 
version information, and package-level imports.
"""

# Project version
__version__ = "0.1.0"

# Define what gets imported when someone does 'from energysim import *'
__all__ = ['core', 'models', 'utils', 'linalg']

# Import key classes or functions to make them easily accessible
#from .core.data_processor import DataProcessor
from .models.matvec import flat_matrix_vector_multiply, flat_mv_spm, EnergyDatabase, StoredProgramMachineEnergy
from .utils.logger import get_logger, LoggingContext, LoggerConfig
from .linalg.vector import Vector
from .linalg.matrix import Matrix