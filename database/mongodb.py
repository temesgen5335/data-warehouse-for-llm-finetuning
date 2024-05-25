import os
from dotenv import load_dotenv
from pymongo import MongoClient

class MongoDB:
    def __init__(self, collection_name: str = None, db_name: str = None):
        load_dotenv()
        # TODO Add error handling for missing environment variables and arguments
        # provide the mongodb atlas url to connect python to mongodb using pymongo
        self.CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
        self.MONGO_DB_NAME = os.getenv("MONGO_DB_NAME") if db_name is None else db_name
        self.MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME") if collection_name is None else collection_name

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        self.client = MongoClient(self.CONNECTION_STRING)
        self.db = self.client[self.MONGO_DB_NAME]
        self.collection = self.db[self.MONGO_COLLECTION_NAME]

    def get_database(self):
        # Create the database
        return self.client[self.MONGO_DB_NAME]

    def create_collection(self, collection_name: str = None):
        collection_name = self.MONGO_COLLECTION_NAME if collection_name is None else collection_name
        # Create the database
        db = self.client[self.MONGO_DB_NAME]

        # Create the collection
        return db[collection_name]

    def get_content(self, filter_col: dict = None, collection_name: str = None):
        collection_name = self.MONGO_COLLECTION_NAME if collection_name is None else collection_name
        # Get content from MongoDB
        collection = self.create_collection(collection_name)

        return collection.find_one(filter_col)
    
    def get_all_content(self, filter_col: dict = None, collection_name: str = None):
        collection_name = self.MONGO_COLLECTION_NAME if collection_name is None else collection_name
        # Get all content from MongoDB
        collection = self.create_collection(collection_name)

        return collection.find(filter_col)

    def get_all_content_as_list(self, filter_col: dict = None, collection_name: str = None):
        collection_name = self.MONGO_COLLECTION_NAME if collection_name is None else collection_name
        # Get all content from MongoDB
        collection = self.create_collection(collection_name)

        return list(collection.find(filter_col))

    def insert_content(self, content: dict, collection_name: str = None):
        collection_name = self.MONGO_COLLECTION_NAME if collection_name is None else collection_name
        # Insert content into MongoDB
        collection = self.create_collection(collection_name)

        return collection.insert_one(content)