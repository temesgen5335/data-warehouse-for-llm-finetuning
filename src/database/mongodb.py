import os
from dotenv import load_dotenv
from pymongo import MongoClient

class MongoDB:
    def __init__(self, collection_name: str = None, db_name: str = None, connection_string: str = None, client=None):
        load_dotenv()
        # TODO Add error handling for missing environment variables and arguments
        # provide the mongodb atlas url to connect python to mongodb using pymongo
        self.CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING") if connection_string is None else connection_string
        self.MONGO_DB_NAME = os.getenv("MONGO_DB_NAME") if db_name is None else db_name
        self.MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME") if collection_name is None else collection_name

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        self.client = MongoClient(self.CONNECTION_STRING) if client is None else client
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

    def insert_many_content(self, content: list[dict], collection_name: str = None):
        collection_name = self.MONGO_COLLECTION_NAME if collection_name is None else collection_name
        # Insert content into MongoDB
        collection = self.create_collection(collection_name)

        return collection.insert_many(content)
    
    def find_one(self, filter_col=None):
        return self.collection.find_one(filter_col)
    
    def delete_one(self, filter_col=None):
        return self.collection.delete_one(filter_col)
    
    def find(self, filter_col=None, collection_name=None):
        collection_name = self.MONGO_COLLECTION_NAME if collection_name is None else collection_name
        collection = self.create_collection(collection_name)
        return collection.find(filter_col)
    
    def save_content_to_txt(self, fields: list[str], filter_col: dict = None, collection_name: str = None, output_file: str = 'output.txt'):
        # Get all content from MongoDB
        documents = self.get_all_content(filter_col, collection_name)

        # Open the output file
        with open(output_file, 'w') as f:
            # Iterate over the documents
            for doc in documents:
                # Concatenate the data from the given fields
                text = ' '.join(doc[field] for field in fields if field in doc)

                # Preprocess the text here (e.g., remove irrelevant characters, normalize case, etc.)

                # Write the preprocessed text to the file, followed by a newline
                f.write(text + '\n')


    def remove_duplicates(self, field: str, collection_name:str =None):
        # If no collection name is provided, use self.collection
        collection = self.db[collection_name] if collection_name else self.collection

        pipeline = [
            { "$group": {
                "_id": { field: f"${field}" },  
                "uniqueIds": { "$addToSet": "$_id" },
                "count": { "$sum": 1 }
            }},
            { "$match": {
                "count": { "$gt": 1 }
            }}
        ]

        duplicates = collection.aggregate(pipeline)

        for duplicate in duplicates:
            ids_to_remove = duplicate['uniqueIds'][1:]  # keep the first one, remove the rest
            for id_to_remove in ids_to_remove:
                collection.delete_one({'_id': id_to_remove})