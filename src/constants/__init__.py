import os
from datetime import datetime
from dotenv import load_dotenv
from from_root import from_root

ROOT_DIR = from_root()

env_file_path = os.path.join(ROOT_DIR, '.env')
load_dotenv(env_file_path)

# MongoDB
DATABASE_NAME='ner-mlops'
COLLECTION_NAME='ner-mlops-data'
MONGODB_URI=os.getenv('MONGODB_URI')

#Logging
LOG_DIR='logs'
LOG_FILENAME = f"{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}.log"
MAX_LOG_SIZE=5*1024*1024
BACKUP_COUNT=3

#Azure
BLOB_STORAGE_REGION='eastasia'
BLOB_STORAGE_INSTANCE_NAME=os.getenv('BLOB_STORAGE_INSTANCE_NAME')
AZURE_TENANT_ID=os.getenv('AZURE_TENANT_ID')
AZURE_CLIENT_ID=os.getenv('AZURE_CLIENT_ID')
AZURE_CLIENT_SECRET=os.getenv('AZURE_CLIENT_SECRET')
AZURE_STORAGE_ACCOUNT_URL=os.getenv('AZURE_STORAGE_ACCOUNT_URL')

#Pipeline
PIPELINE_NAME: str = ''
ARTIFACT_DIR: str = 'artifact'

# Files
MODEL_FILE_NAME: str = 'model.h5' 
OUTPUT_MODEL_NAME: str = 'model.onnx'
FILE_NAME: str = 'data.csv'
TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'

SCHEMA_FILE_PATH: str = os.path.join('config', 'schema.yaml')

# Data Ingestion
DATA_INGESTION_COLLECTION_NAME: str = 'Project1-Data'
DATA_INGESTION_DIR_NAME: str = 'data_ingestion'
DATA_INGESTION_RAW_DATA_DIR: str = 'raw_data'

DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_REPORT_FILE_NAME: str = 'report.yaml'

