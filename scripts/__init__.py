# scripts/__init__.py

"""
Scripts environment initialization.
This file can include
version information, and package-level imports.
"""
import os
import sys

# Add project source directory to Python path
# This ensures scripts can import from the project package
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src/energysim'))
print(project_root)
sys.path.insert(0, project_root)

print(sys.path)

