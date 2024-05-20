import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")


def get_database(db_name: str):
    # provide the mongodb atlas url to connect python to mongodb using pymongo

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database
    return client[db_name]


def get_collection(db_name: str, collection_name: str):
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database
    db = client[db_name]

    # Create the collection
    return db[collection_name]
