import os
import json

from pandas import DataFrame, read_csv

from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import read_yaml_file
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.constants import SCHEMA_FILE_PATH
 
logger = logging.getLogger('Data Validation')
 
class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e)
    
    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        """Validates the number of columns.
        Returns: bool
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config['columns'])
            return status
        except Exception as e:
            raise CustomException(e)
    
    def is_column_present(self, dataframe: DataFrame) -> bool:
        """Checks if all different type of required columns are present
        
        Returns: bool
        """
        try:
            columns = dataframe.columns
            missing_categorical_columns = []
            # checking if all categorical columns are present
            for column in self._schema_config['categorical_columns']:
                if column not in columns:
                    missing_categorical_columns.append(column)
            
            if  len(missing_categorical_columns)>0:
                logger.error(f'{len(missing_categorical_columns)} categorical columns are missing!')
            
            return False if len(missing_categorical_columns)>0 else True
        except Exception as e:
            raise CustomException(e)
        
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        """Initiates DataValidation.
        Returns: bool value based on validation results
        """
        try:
            logger.info('Validating Data...')
            dataframe = read_csv(self.data_ingestion_artifact.raw_data_file_path)
            
            validation_success = True
            validation_msg = ''
            
            status = self.validate_number_of_columns(dataframe)
            logger.info(f'Status for all columns are present is {status}.')
            if not status:
                validation_success = False
                validation_msg += 'Some columns are missing!. '
            else:
                validation_msg += 'All columns are present. '
            
            status = self.is_column_present(dataframe)
            if status:
                logger.info('All categorical columns are present.')
                validation_msg += 'All categorical columns are present. '
            else:
                validation_success = False
                validation_msg += 'Some categorical columns are missing!'
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_success,
                message=validation_msg,
                validation_report_file_path=self.data_validation_config.validation_report_file_path)
            
            report_dir = os.path.dirname(self.data_validation_config.validation_report_file_path)
            os.makedirs(report_dir, exists_ok=True)
            
            validation_report = {
                'validation_status': validation_success,
                'message': validation_msg
            }
            
            with open(self.data_validation_config.validation_report_file_path, 'w') as file:
                json.dump(validation_report, file, indent=4)
                
            logger.info('Data Validation Artifact created and saved as JSON file.')
            logger.info(f'Data validation artifact: {data_validation_artifact}')
            
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e)