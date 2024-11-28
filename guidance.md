I'll explain the purpose and typical content of `__init__.py` files at different levels of a Python project.

1. Project Root `__init__.py`
```python
# src/my_project/__init__.py

"""
Project-level initialization.
This file can include project-wide configurations, 
version information, and package-level imports.
"""

# Project version
__version__ = "0.1.0"

# Optional: Define what gets imported when someone does 'from my_project import *'
__all__ = ['core', 'models', 'utils']

# Optional: Import key classes or functions to make them easily accessible
from .core.data_processor import DataProcessor
from .models.user_model import User
from .utils.logging import setup_logging

```

2. Subpackage `__init__.py` (e.g., in `core/`, `models/`, `utils/`)
```python
# src/my_project/core/__init__.py

"""
Core package initialization.
Helps organize and expose key components of the subpackage.
"""

# Import key classes or functions to make them easily accessible
from .data_processor import DataProcessor
from .helpers import validate_data

# Optional: Define what gets imported with wildcard import
__all__ = ['DataProcessor', 'validate_data']

```

3. Tests `__init__.py`
```python
# tests/__init__.py

"""
Test package initialization.
Can include test-wide configurations or helpers.
"""

import os
import sys

# Add project source directory to Python path
# This ensures tests can import from the project package
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
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

```

Purpose of `__init__.py`:
1. Mark directories as Python packages
2. Initialize package-level configurations
3. Control what gets imported
4. Provide package-level imports and utilities

Best Practices:
- Keep `__init__.py` files minimal
- Use for package-level configurations
- Import key classes/functions to simplify imports
- Avoid complex logic or heavy computations

Common Use Cases:
- Define package version
- Set up logging
- Import key classes
- Configure package-level settings
- Create convenience imports

Minimal `__init__.py`:
```python
# Can be completely empty - just marks the directory as a package
```

Advanced Techniques:
- Lazy loading of modules
- Dynamic import configurations
- Package-level error handling
