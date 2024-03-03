from typing import Any

from pymongo import MongoClient

from src.application import log
from src.application.environment import read_database_environment


logger = log.get_logger(__name__)

environment = read_database_environment()
        
user = environment["MONGO_USER"]
password = environment["MONGO_PASSWORD"]
host = environment["MONGO_HOST"]
database_name = environment["MONGO_DATABASE"]

class DatabaseConnection:
    def __init__(self) -> None:
        string_connection =  f"mongodb://{user}:{password}@{host}:27017/{database_name}?authSource=admin&retryWrites=true&w=majority"
        self.client = MongoClient(
            string_connection, tz_aware=True
        )
        logger.debug(f"Database {string_connection} connected successfully")

    def aggregate(self, collection: str, pipeline, **kwargs: Any):
        return list(self.client[database_name][collection].aggregate(pipeline=pipeline))

    def find(self, collection: str, select: dict[str, Any], **kwargs: Any):
        return self.client[database_name][collection].find(select, **kwargs)
    
    def find_one(self, collection: str, select: dict[str, Any], **kwargs: Any):
        return self.client[database_name][collection].find_one(select, **kwargs)

    def insert_one(self, collection: str, document):
        return self.client[database_name][collection].insert_one(document)
    
    def update_one(self, collection: str, select: dict[str, Any], update: dict[str, Any]):
        return self.client[database_name][collection].update_one(select, update)

    def delete_one(self, collection: str, select: dict[str, Any]):
        return self.client[database_name][collection].delete_one(select)
    

database = DatabaseConnection()
