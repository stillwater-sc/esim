# A logging design that demonstrates best practices for logging in a Python application.

How to use this logging utility:

```python
# Example usage in another module
from esim.utils.logging import get_logger, LoggingContext

# Basic logging
logger = get_logger(__name__)

def process_data(data):
    """
    Example function demonstrating logging
    """
    try:
        logger.info("Starting data processing")
        
        # Debug-level logging
        logger.debug(f"Processing data: {data}")
        
        # Simulate some processing
        result = [x * 2 for x in data]
        
        logger.info(f"Processed {len(result)} items")
        return result
    
    except Exception as e:
        # Error logging
        logger.error(f"Error processing data: {e}", exc_info=True)
        raise

def advanced_logging_example():
    """
    Demonstrate advanced logging techniques
    """
    # Temporary logging context
    with LoggingContext(logger, level='DEBUG') as temp_logger:
        # This block will use DEBUG level logging
        temp_logger.debug("This is a debug message that would normally be suppressed")
    
    # Outside the context, logging returns to its original level
    logger.debug("This won't be logged if original level was INFO or higher")

# Example of adding a temporary handler
def log_to_file_temporarily():
    # Create a temporary file handler
    file_handler = logging.FileHandler('temporary_log.log')
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(message)s')
    )
    
    # Use logging context to add temporary handler
    with LoggingContext(logger, handler=file_handler):
        logger.info("This will be logged to both console and temporary file")

```

Key Features of this Logging Design:

1. Flexible Configuration
- Configurable log levels
- Optional console and file logging
- Rotating file logs to manage disk space

2. Advanced Logging Utilities
- `LoggerConfig`: Centralized logger setup
- `LoggingContext`: Temporary logging configuration
- Easily customizable logging behavior

3. Best Practices
- Type hinting
- Comprehensive error handling
- Flexible log file management

Recommended Usage:
```python
# In any module
from esim.utils.logging import get_logger

# Create a logger specific to the module
logger = get_logger(__name__)

# Log messages
logger.info("Starting process")
logger.debug("Detailed information")
logger.error("Something went wrong")
```

Configuration Options:
- Adjust log levels
- Control console/file output
- Set log file size and backup count
- Add custom formatting
