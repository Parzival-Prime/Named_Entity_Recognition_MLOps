import os
from src.logger import logging
from src.exception import handle_exception, CustomException
from src.configuration.azure_connection import CreateBlobServiceClient

from azure.core.exceptions import ResourceNotFoundError, ServiceRequestError, AzureError

import pickle

logger = logging.getLogger('Azure Storage Service')

class AzureBlobStorage:
    """A Class to interact with Azure Blob Storage Account, for data upload and retrieval."""
    
    def __init__(self):
        self.blob_service_client = CreateBlobServiceClient().blob_service_client
        
    @handle_exception
    def is_file_available(self, container_name: str, file_path: str) -> bool:
        """Checks is the Storage Container is available.
        
        Arguments:
            container_name(str): Name of the Azure blob container.
            file_name(str): Name of the file.
        
        Returns:
            Bool: True if file exits, False otherwise
        """
        
        try:
            logger.info('Checking resource...')
            
            azure_logger = logging.getLogger('azure.core.pipeline.policies.http_logging_policy')
            azure_logger.setLevel(logging.WARNING)  # or ERROR to suppress more
            # Optional: Suppress urllib3 if using requests under the hood
            urllib_logger = logging.getLogger("urllib3")
            urllib_logger.setLevel(logging.WARNING)
            
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=file_path)
            blob_client.get_blob_properties()
            
            logger.info('Resource is available!')
            return True
        except ResourceNotFoundError:
            logger.error('Resource Not Found!')
            return False
    
    
    @handle_exception
    def upload_file(self, file_path: str, file_blob_name: str,  container_name: str, file_blob_dir: str=None, remove: bool=True) -> None:
        """This method uploads file to Azure Storage Service.
        
        Arguments:
            from_directory(str): Path of the local file.
            to_directory(str): Target file path in the bucket.
            container_name(str): Name of the Container.
            remove(bool): If True, deletes the local file after upload.
        """
        try:
            logger.info(f'Uploading file from {file_path} to {file_blob_dir | 'top_directory'} in {container_name} blob storage container on Azure...')
            
            azure_logger = logging.getLogger('azure.core.pipeline.policies.http_logging_policy')
            azure_logger.setLevel(logging.WARNING)  # or ERROR to suppress more
            # Optional: Suppress urllib3 if using requests under the hood
            urllib_logger = logging.getLogger("urllib3")
            urllib_logger.setLevel(logging.WARNING)
            
            uploading_model_path = os.path.join(file_blob_dir, file_blob_name)
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=uploading_model_path)
            
            blob_client.upload_blob(data=open(file_path, 'rb'), overwrite=True)
            logger.info('file uploaded Successfully!')
            
            if remove:
                os.remove(file_path)
                logging.info(f'Local file {file_path} deleted after upload!')
            
        except ServiceRequestError as e:
            logging.error('There is a network error os DNS faliure, client cannot reach the Azure service.')
            raise CustomException(e)
        except AzureError as e:
            logging.error('There is some kind of Azure Error!')
            raise CustomException(e)
        except Exception as e:
            logging.error('An Unexpected Error occured!')
            raise CustomException(e)
        
        
    @handle_exception
    def download_file(self, file_blob_name: str, container_name: str, file_save_path: str, file_blob_dir: str=None) -> object:
        """Downloads the specified model stored on Azure Blob Storage.
        
        Arguments:
            model_name(str): Name of the model file.
            container_name(str): Name of the Container in which model is stored.
            model_directory(str): Path of the model file in the container.
            
        Returns:
            object: Model object.
        """
        try:
            logger.info('Downloading Model...')
            
            if file_blob_dir is not None:
                file_path = os.path.join(file_blob_dir, file_blob_name)
            else:
                file_path = file_blob_name
                
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=file_path)
            
            blob_data = blob_client.download_blob().readall()
            
            with open(file_save_path, 'wb') as model_file:
                pickle.dump(blob_data, model_file)
                
        except ResourceNotFoundError as e:
            logging.error('ResourceError! Blob not found in container.')
            raise CustomException(e)
        except ServiceRequestError as e:
            logging.error('There is a network error os DNS faliure, client cannot reach the Azure service.')
            raise CustomException(e)
        except AzureError as e:
            logging.error('There is some kind of Azure Error!')
            raise CustomException(e)
        except Exception as e:
            logging.error('An Unexpected Error occured!')
            raise CustomException(e)