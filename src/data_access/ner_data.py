import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import CustomException

class NerData:
    """A Class to import MongoDB Records as pandas DataFrame."""
    
    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise CustomException(e)
        
    def export_collection_as_DataFrame(self, collection_name: str, database_name: Optional[str]=None) -> pd.DataFrame:
        """Exports an Entire MongoDB Collection as Pandas DataFrame.
        
        Parameters
        ----------
        collection_name: str
            The name of the MongoDB collection to export.
        database_name: Optional[str]
            Name of the Database (Optional). Defaults to DATABASE_NAME.
            
        Returns
        -------
        pd.DataFrame
        """
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            # Changing the name of Column 'Sentence #' to 'Sentence'
            df.rename(columns={'Sentence #': 'Sentence'}, inplace=True)
            df.replace({'na': np.nan}, inplace=True)
            return df
        except Exception as e:
            raise CustomException(e)