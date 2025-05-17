from src.logger import logging
import traceback

logger = logging.getLogger('exception')



class CustomException(Exception):
    """Base class for Custom Exceptions"""
    
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        
        
def log_exception(e):
    """Logs the exception with traceback"""
    logger.error(f'Exception occured: {str(e)}')
        
def handle_exception(func):
    """Decorator to handle and log exceptions for any function"""
    
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomException as ce:
            log_exception(ce) # type: ignore
        except Exception as e:
            log_exception(e) # type: ignore
    
    return wrapper