import os
from datetime import datetime
from dotenv import load_dotenv #type: ignore

load_dotenv()

# MongoDB
DATABASE_NAME='ner-mlops'
COLLECTION_NAME='ner-mlops-data'
MONGODB_URI=os.getenv('MONGODB_URI')

#Logging
LOG_DIR='logs'
LOG_FILENAME = f"{datetime.now().strftime('%d-%m-%Y--%H-%M-%S')}.log"
MAX_LOG_SIZE=5*1024*1024
BACKUP_COUNT=3

#Azure
BLOB_STORAGE_REGION='eastasia'
BLOB_STORAGE_INSTANCE_NAME=os.getenv('BLOB_STORAGE_INSTANCE_NAME')
AZURE_TENANT_ID=os.getenv('AZURE_TENANT_ID')
AZURE_CLIENT_ID=os.getenv('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET=os.getenv('AZURE_CLIENT_SECRET')
AZURE_STORAGE_ACCOUNT_URL=os.getenv('AZURE_STORAGE_ACCOUNT_URL')
