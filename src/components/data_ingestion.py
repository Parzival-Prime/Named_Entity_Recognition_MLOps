import os

from pandas import DataFrame, read_csv
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.exception import CustomException
from src.logger import logging
from src.data_access.ner_data import NerData

logger = logging.getLogger('Data Ingestion')


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig=DataIngestionConfig()):
        self.data_ingestion_config = data_ingestion_config
        
        
    def export_data_into_feature_store(self) -> DataFrame:
        """This Method Imports data from mongodb to a csv file, and saves it to feature store.

            Returns
            -------
                Data is returned as pandas DataFrame.
        """
        try:
            logger.info('Import data from MonngoDB...')
            my_data = NerData()
            
            dataframe = my_data.export_collection_as_DataFrame(collection_name=self.data_ingestion_config.collection_name)
            logger.info(f'Data Imported of shape: {dataframe.shape}')
            
            raw_data_file_path = self.data_ingestion_config.raw_data_file_path
            dir_name = os.path.join(raw_data_file_path)
            os.makedirs(dir_name, exist_ok=True)
            
            logger.info('Saving Imported Data into feature store')
            dataframe.to_csv(raw_data_file_path, index=False, header=True)
            
            return dataframe
        except Exception as e:
            logger.error('Error Occured While Importing Data from MongoDB')
            raise CustomException(e)
        
        
    # def split_data_as_train_test(self, dataframe: DataFrame) -> None:
    #     """This method splits dataframe into train and test portion in split ratio."""
        
    #     try:
    #         logger.info('Performing train test split...')
            
    #         if len(dataframe) == 0:
    #             raise ValueError('DataFrame is empty, cannot split empty dataset.')
            
    #         train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            
    #         logger.info('Exporting train and test sets...')
            
    #         dir_path = os.path.dirname(self.data_ingestion_config.train_set_file_path)
    #         os.makedirs(dir_path, exists_ok=True)
    #         dir_path = os.path.join(self.data_ingestion_config.test_set_file_path)
    #         os.makedirs(dir_path, exists_ok=True)
            
    #         train_set.to_csv(self.data_ingestion_config.train_set_file_path, index=False, header=True)
    #         test_set.to_csv(self.data_ingestion_config.test_set_file_path, index=False, header=True)
            
    #         logger.info('train test files Exported!')
            
        except Exception as e:
            logger.error('Error occured while Spliting dataframe into train test.')
            raise CustomException(e)
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """This method initiates the data ingestion components of training pipeline.
        
        Returns
        -------
            Train and Test sets are returned as data ingestion artifacts.
        """
        try:
            logger.info('Initiating Data Ingestion....')
            dataframe = self.export_data_into_feature_store()
            # self.split_data_as_train_test(dataframe)
            
            data_ingestion_artifact = DataIngestionArtifact(raw_data_file_path=self.data_ingestion_config.raw_data_file_path)
            
            logging.info(f'Data Ingestion Artifact: {data_ingestion_artifact}')
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e)
        