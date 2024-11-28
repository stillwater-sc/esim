# tests/__init__.py

"""
Test package initialization.
Can include test-wide configurations or helpers.
"""

import os
import sys

# Add project source directory to Python path
# This ensures tests can import from the project package
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src/energysim'))
sys.path.insert(0, project_root)

# Optional: Shared test utilities
def create_temp_data():
    """
    Helper function to create temporary test data.
    """
    pass

# Optional: Pytest configurations or global fixtures
def pytest_configure(config):
    """
    Optional pytest configuration hook.
    """
    config.addinivalue_line(
        "markers", "slow: mark test as slow-running"
    )
