import os
from datetime import datetime
from dotenv import load_dotenv #type: ignore


# MongoDB
DATABASE_NAME='ner-mlops'
COLLECTION_NAME='ner-mlops-data'
MONGODB_URI='MONGODB_URI'

#Logging
LOG_DIR='logs'
LOG_FILENAME=f'{datetime.now().strftime('%d-%m-%Y--%H-%M-%S')}.log'
MAX_LOG_SIZE=5*1024*1024
BACKUP_COUNT=3

