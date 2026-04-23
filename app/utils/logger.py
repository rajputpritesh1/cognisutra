"""
Logging configuration for Cognisutra
"""

import logging
import logging.handlers
import os
from datetime import datetime

class LoggerSetup:
    """Setup logging for the application"""
    
    @staticmethod
    def setup_logger(app=None, log_level=logging.DEBUG):
        """Configure application logging"""
        
        # Create logs directory if it doesn't exist
        logs_dir = 'logs'
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Create file handler for all logs
        file_handler = logging.handlers.RotatingFileHandler(
            filename=f'{logs_dir}/cognisutra.log',
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        
        # Create error file handler
        error_handler = logging.handlers.RotatingFileHandler(
            filename=f'{logs_dir}/errors.log',
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        
        # Create console handler for development
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        
        # Get root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # Clear existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Add handlers
        root_logger.addHandler(file_handler)
        root_logger.addHandler(error_handler)
        root_logger.addHandler(console_handler)
        
        if app:
            app.logger.setLevel(log_level)
        
        return root_logger
    
    @staticmethod
    def get_logger(name):
        """Get logger for a specific module"""
        return logging.getLogger(name)
