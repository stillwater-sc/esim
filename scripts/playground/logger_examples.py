# Example usage in another module
import logging
from energysim import get_logger, LoggingContext

# Basic logger with name=energysim and log_level=logging.INFO
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

if __name__ == '__main__':
    data = [[1,2,3], [4,5,6], "1st", "2nd", "3rd", "4th", "5th", "6th"]
    process_data(data)

    advanced_logging_example()

    log_to_file_temporarily()