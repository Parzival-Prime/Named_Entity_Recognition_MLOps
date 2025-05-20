from src.logger import logging
from src.exception import handle_exception, CustomException
from src.configuration.azure_connection import CreateBlobServiceClient

from azure.core.exceptions import ResourceNotFoundError

import pickle

logger = logging.getLogger('Azure Storage Service')

class AzureBlobStorage:
    """A Class to interact with Azure Blob Storage Account, for data upload and retrieval."""
    
    def __init__(self):
        self.blob_service_client = CreateBlobServiceClient().blob_service_client
        
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
    
    def upload_model(self, file_path: str, to_directory: str, container_name: str, remove: bool=True) -> None:
        """This method uploads model to Azure Storage Service.
        
        Arguments:
            from_directory(str): Path of the local file.
            to_directory(str): Target file path in the bucket.
            container_name(str): Name of the Container.
            remove(bool): If True, deletes the local file after upload.
        """
        try:
            logger.info(f'Uploading Model from {file_path} to {to_directory} in {container_name} blob storage container on Azure.')
            
            azure_logger = logging.getLogger('azure.core.pipeline.policies.http_logging_policy')
            azure_logger.setLevel(logging.WARNING)  # or ERROR to suppress more
            # Optional: Suppress urllib3 if using requests under the hood
            urllib_logger = logging.getLogger("urllib3")
            urllib_logger.setLevel(logging.WARNING)
            
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=to_directory)
            
            blob_client.upload_blob(data=open(file_path, "rb"), overwrite=True)
            logger.info('Model uploaded successfully!')
        except Exception as e:
            logger.error('Error occured while uploading model.')
            raise CustomException(e)
        
    def download_model(self, model_name: str, container_name: str, model_directory: str=None) -> object:
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
            model_file = model_directory + '/' + model_name if model_directory else model_name
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=model_file)
            blob_data = blob_client.download_blob().readall()
            model = pickle.loads(blob_data)
            
            return model
        except Exception as e:
            logger.error('Error occured while downloading model.')
            raise CustomException(e)