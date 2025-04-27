from src.logger import logging
from demo1 import second_file_func

logger = logging.getLogger('demo')

logger.info('This is from demo.py')
second_file_func()