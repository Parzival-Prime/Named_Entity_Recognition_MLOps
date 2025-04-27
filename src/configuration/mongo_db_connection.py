import os
import sys

import pymongo
import certifi

import pymongo
from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONOGDB_URI

ca = certifi.where()

logger = logging.getLogger('mongodb_connection')

class MongoDBClient:
    """
    MongoDBClient is responsible for establishing a connection with MongoDB Database
    
    Attributes:
    ------------
    client : MongoClient
        A shared MongoClient instance for the class
    database : Database
        The specific database instance that MongoDBClient connects to.
        
    Methods:
    ---------
    __init__ : 
        Initializes the MongoDB connection using the given database name.
        
        params:
            database_name : str
        return:
            None
    """
    
    client = None
    
    def __init__(self, database_name: str = DATABASE_NAME, mongodb_connection_uri: str = MONOGDB_URI) -> None:
        """
        Initializes a connection to MongoDB Database. If no existing connection is found it establishes a new one.
        
        parameters:
        -----------
        database_name : str, Optional 
            Name of the MongoDB Database to connect to. Default is set to DATABASE_NAME constant
        """
        
        try:
            if MongoDBClient.client is None:
                if mongodb_connection_uri is None:
                    raise Exception(f'Environment variable {MONOGDB_URI} is not set.')
                
                MongoDBClient.client = pymongo.MongoClient(mongodb_connection_uri, tlsCAFile=ca)
            
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logger.info('MongoDB connection successful.')
                
        except Exception as e:
            raise MyException(e, sys)