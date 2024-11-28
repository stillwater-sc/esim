# src/energysim/linalg/__init__.py

"""
Linalg package initialization.
Helps organize and expose key components of the subpackage.
"""

# Import key classes or functions to make them easily accessible
from vector import Vector

# Define what gets imported with wildcard import
__all__ = ['vector', 'matrix']

