import pytest
from pymongo.errors import DuplicateKeyError
from mongomock import MongoClient

import os

os.chdir('../')

# import the MongoDB class from the database.mongodb module
from database.mongodb import MongoDB

class TestMongoDB:
    # Create a fixture to mock the database
    @pytest.fixture(autouse=True)
    def mock_db(self):
        client = MongoClient()
        yield client

    def setup_method(self, method):
        self.mongodb = MongoDB(collection_name='test_collection', db_name='test_db')
        self.mongodb.collection.drop()

    def test_get_database(self, mock_db):
        db = self.mongodb.get_database()
        # Check if the database is created with the correct name
        assert db.name == mock_db['test_db'].name

    def test_create_collection(self, mock_db):
        collection = self.mongodb.create_collection('test_collection')
        # Check if the collection is created with the correct name
        assert collection.name == mock_db['test_db']['test_collection'].name

    def test_insert_content(self, mock_db):
        content = {"key": "value"}
        result = self.mongodb.insert_content(content)
        # Check if the content is inserted successfully
        assert result.acknowledged == True
    
    def test_get_content(self, mock_db):
        content = {"key": "value"}
        self.mongodb.insert_content(content)
        result = self.mongodb.get_content()
        # Remove the '_id' field from the result and content before comparing
        result.pop('_id', None)
        content.pop('_id', None)
        # Check if the content is retrieved successfully
        assert result == content

    def test_get_all_content(self, mock_db):
        content = [{"key": "value1"}, {"key": "value2"}]
        for c in content:
            self.mongodb.insert_content(c)
        results = list(self.mongodb.get_all_content())
        # Remove the '_id' field from the results and content before comparing
        for r in results:
            r.pop('_id', None)
        for c in content:
            c.pop('_id', None)
        
        # Check if all content is retrieved successfully
        assert results == content

    def test_get_all_content_as_list(self, mock_db):
        content = [{"key": "value1"}, {"key": "value2"}]
        for c in content:
            self.mongodb.insert_content(c)
        results = self.mongodb.get_all_content_as_list()
        # Remove the '_id' field from the results and content before comparing
        for r in results:
            r.pop('_id', None)
        for c in content:
            c.pop('_id', None)
        
        # Check if all content is retrieved successfully
        assert results == content