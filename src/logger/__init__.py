import os
import logging
from logging.handlers import RotatingFileHandler
from from_root import from_root #type: ignore

from src.constants import LOG_DIR, LOG_FILENAME, MAX_LOG_SIZE, BACKUP_COUNT

log_dir_path = os.path.join(from_root(), LOG_DIR)
os.makedirs(log_dir_path, exist_ok=True)


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