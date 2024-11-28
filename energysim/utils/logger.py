# energysim/utils/logger.py
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional, Union, TextIO

class LoggerConfig:
    """
    Centralized logging configuration for the entire project.
    Provides flexible logging setup with multiple outputs and configurations.
    """
    
    @staticmethod
    def setup_logger(
        name: str = 'energysim',
        log_level: Union[str, int] = logging.INFO,
        log_dir: Optional[str] = None,
        console_output: bool = True,
        file_output: bool = True,
        max_file_size_bytes: int = 10 * 1024 * 1024,  # 10 MB
        backup_count: int = 5
    ) -> logging.Logger:
        """
        Configure a logger with customizable outputs and settings.
        
        :param name: Name of the logger
        :param log_level: Logging level (e.g., logging.INFO, 'DEBUG')
        :param log_dir: Directory for log files (creates if not exists)
        :param console_output: Enable console logging
        :param file_output: Enable file logging
        :param max_file_size_bytes: Maximum size of log file before rotation
        :param backup_count: Number of backup log files to keep
        :return: Configured logger instance
        """
        # Ensure log level is an integer
        if isinstance(log_level, str):
            log_level = getattr(logging, log_level.upper())
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        
        # Clear any existing handlers to prevent duplicate logging
        logger.handlers.clear()
        
        # Formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console Handler
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(log_level)
            logger.addHandler(console_handler)
        
        # File Handler
        if file_output:
            # Create log directory if it doesn't exist
            if log_dir is None:
                log_dir = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), 
                    '..', 
                    '..', 
                    'logs'
                )
            
            # Ensure log directory exists
            os.makedirs(log_dir, exist_ok=True)
            
            log_file_path = os.path.join(log_dir, f'{name}.log')
            
            # Rotating File Handler
            file_handler = RotatingFileHandler(
                log_file_path, 
                maxBytes=max_file_size_bytes, 
                backupCount=backup_count
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(log_level)
            logger.addHandler(file_handler)
        
        return logger

class LoggingContext:
    """
    Context manager for temporary logging configuration.
    Allows for temporary logging adjustments within a specific block.
    """
    
    def __init__(
        self, 
        logger: logging.Logger, 
        level: Union[int, str] = None, 
        handler: Optional[logging.Handler] = None
    ):
        """
        :param logger: Logger to modify
        :param level: Temporary logging level
        :param handler: Temporary handler to add
        """
        self.logger = logger
        self.original_level = logger.level
        self.level = level
        self.handler = handler
    
    def __enter__(self):
        # Set temporary logging level if provided
        if self.level is not None:
            if isinstance(self.level, str):
                self.level = getattr(logging, self.level.upper())
            self.logger.setLevel(self.level)
        
        # Add temporary handler if provided
        if self.handler:
            self.logger.addHandler(self.handler)
        
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore original logging level
        self.logger.setLevel(self.original_level)
        
        # Remove temporary handler if it was added
        if self.handler:
            self.logger.removeHandler(self.handler)

def get_logger(
    name: str = 'energysim',
    log_level: Union[str, int] = logging.INFO
) -> logging.Logger:
    """
    Convenience function to get a logger with default configuration.
    
    :param name: Name of the logger
    :param log_level: Logging level
    :return: Configured logger
    """
    return LoggerConfig.setup_logger(name=name, log_level=log_level)
