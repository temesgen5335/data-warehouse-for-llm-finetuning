import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = MongoClient(CONNECTION_STRING)

def get_database(db_name: str):
    # Create the database
    return client[MONGO_DB_NAME]


def get_collection(db_name: str, collection_name: str):
    # Create the database
    db = client[db_name]

    # Create the collection
    return db[collection_name]


def get_content(db_name: str, collection_name: str, filter_col: dict = None):
    # Get content from MongoDB
    collection = get_collection(db_name, collection_name)

    return collection.find_one(filter_col)
