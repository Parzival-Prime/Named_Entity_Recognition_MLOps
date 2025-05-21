import os
from src.logger import logging
from src.exception import handle_exception, CustomException
from src.configuration.azure_connection import CreateBlobServiceClient

from azure.core.exceptions import ResourceNotFoundError, ResourceExistsError, ServiceRequestError, AzureError

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
            logger.info('checking resource...')
            
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=file_path)
            blob_client.get_blob_properties()
            
            logging.info('Resource is available!')
            return True
        except ResourceNotFoundError as e:
            logging.error('Resource not available!')
            raise CustomException(e)
        except Exception as e:
            logging.error('Some error occured in function "is_file_available" in azure_storage.py!')
            raise CustomException(e)
        
        
    @handle_exception
    def upload_file(self, file_path: str, file_blob_path: str,  container_name: str, remove: bool=True) -> None:
        """This method uploads file to Azure Storage Service.
        
        Arguments:
            file_path(str): Path of the local file.
            file_blob_path(str): file path in the container to upload.
            container_name(str): Name of the Container.
            remove(bool): If True, deletes the local file after upload.
        """
        try:
            logger.info(f'Uploading file from {file_path} to {file_blob_path} in {container_name} blob storage container on Azure...')
            
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=file_blob_path)
            
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
    def download_file(self, file_blob_path: str, container_name: str, file_save_path: str) -> object:
        """Downloads the specified model stored on Azure Blob Storage.
        
        Arguments:
            file_blob_path(str): Path of the file in the container.
            container_name(str): Name of the Container in which model is stored.
            file_save_path(str): Path where file is to be saved.
            
        Returns:
            just downloads the file in specified path.
        """
        try:
            logger.info('Downloading Model...')
            
            file_status = self.is_file_available(container_name=container_name, file_path=file_blob_path)
            if not file_status:
                raise ResourceNotFoundError
                
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=file_blob_path)
            
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
        
    
    @handle_exception
    def create_container(self, container_name: str):
        """Creates a new container in Storage Account.
        
        Parameters
        ----------
        container_name(str): Name of the container to create
        
        Returns
        -------
        returns nothing just creates container.
        """
        try:
            logger.info(f'Creating new container "{container_name}"')
            container_client = self.blob_service_client.create_container(container_name)
            logger.info('Container created Successfully!')
        except ResourceExistsError as e:
            logger.error(f'Container with name {container_name} already exits!')
        except ServiceRequestError as e:
            logger.error('There is a network error os DNS faliure, client cannot reach the Azure service.')
            raise CustomException(e)
        except AzureError as e:
            logger.error('Some Azure Error Occured!')
            raise CustomException(e)
        except Exception as e:
            logger.error('An Unexpected Error occured!')
            raise CustomException(e)
    
    @handle_exception
    def get_storage_account_info(self):
        """Logs connected Blob Storage accounts info."""
        try:
            logger.info('Fetching Storage Account Info...')
            acc_info = self.blob_service_client.get_account_information()
            logger.info(f'Account Info: {acc_info}')
        
        except Exception as e:
            logger.error('Some error occured!')