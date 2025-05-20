import os
import uuid

from azure.identity import ClientSecretCredential #type: ignore
from azure.storage.blob import BlobServiceClient #type: ignore

from src.constants import AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_STORAGE_ACCOUNT_URL, AZURE_TENANT_ID
from src.exception import CustomException, handle_exception
from src.logger import logging


logger = logging.getLogger('Azure Connection')

class CreateBlobServiceClient:
    
    blob_service_client = None

    @handle_exception
    def __init__(self):
        """This class gets credentials from env vars and establishes connection with Azure Storage Account"""
        
        try: 
            logger.info('Connecting to Azure Storage')
            
            if CreateBlobServiceClient.blob_service_client==None:
                
                __tenant_id = AZURE_TENANT_ID
                __client_id = AZURE_CLIENT_ID
                __client_secret = AZURE_CLIENT_SECRET
                __storage_account_url = AZURE_STORAGE_ACCOUNT_URL
                
                if __tenant_id is None:
                    raise Exception(f"Environment variable {AZURE_TENANT_ID} is not set.")
                if __client_id is None:
                    raise Exception(f"Environment variable {AZURE_CLIENT_ID} is not set.")
                if __client_secret is None:
                    raise Exception(f"Environment variable {AZURE_CLIENT_SECRET} is not set.")
                if __storage_account_url is None:
                    raise Exception(f"Environment variable {AZURE_STORAGE_ACCOUNT_URL} is not set.")
                
                __credential = ClientSecretCredential(
                    tenant_id=__tenant_id,
                    client_id=__client_id,
                    client_secret=__client_secret
                )
                
                CreateBlobServiceClient.blob_service_client = BlobServiceClient(account_url=__storage_account_url, credential=__credential)

            logger.info('Azure Storage Connection Successful!')

        except Exception as e:
            logger.error('Azure Storage Connection Failed')
            raise CustomException(e)