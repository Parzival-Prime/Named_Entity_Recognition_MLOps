import os
import logging
from logging.handlers import RotatingFileHandler
from from_root import from_root #type: ignore

from src.constants import LOG_DIR, LOG_FILENAME, MAX_LOG_SIZE, BACKUP_COUNT

log_dir_path = os.path.join(from_root(), LOG_DIR)
os.makedirs(log_dir_path, exist_ok=True)

# class ConfigureLogger:
#     """Configures logging with a Rotating File Handler and Console Handler"""
    
#     logger = None
#     def __init__(self, file_name:str):
#         self.logger = logging.getLogger(file_name)
#         if ConfigureLogger.logger is None:
#             self.logger.setLevel(logging.DEBUG)
            
#             log_file_path = os.path.join(log_dir_path, LOG_FILENAME)
            
#             formatter = logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s - %(message)s')
            
#             filehandler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
#             filehandler.setFormatter(formatter)
#             filehandler.setLevel(logging.DEBUG)
            
#             consolehandler = logging.StreamHandler()
#             consolehandler.setFormatter(formatter)
#             consolehandler.setLevel(logging.INFO)
            
#             self.logger.addHandler(filehandler)
#             self.logger.addHandler(consolehandler)


def configureLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
        
    log_file_path = os.path.join(log_dir_path, LOG_FILENAME)
        
    formatter = logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s - %(message)s')
        
    filehandler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    filehandler.setFormatter(formatter)
    filehandler.setLevel(logging.DEBUG)
        
    consolehandler = logging.StreamHandler()
    consolehandler.setFormatter(formatter)
    consolehandler.setLevel(logging.INFO)
        
    logger.addHandler(filehandler)
    logger.addHandler(consolehandler)

configureLogger()