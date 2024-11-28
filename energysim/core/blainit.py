# src/esim/core/__init__.py

"""
Core package initialization.
Helps organize and expose key components of the subpackage.
"""

# Import key classes or functions to make them easily accessible
from .data_processor import DataProcessor
# from .helpers import validate_data

# Optional: Define what gets imported with wildcard import
# __all__ = ['DataProcessor', 'validate_data']
__all__ = ['DataProcessor']