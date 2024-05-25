import pytest
from pymongo.errors import DuplicateKeyError
from mongomock import MongoClient

import os

os.chdir('../')

# import the MongoDB class from the database.mongodb module
from database.mongodb import MongoDB

# Create a fixture to mock the database
@pytest.fixture
def mock_db():
    client = MongoClient()
    yield client

def test_get_database(mock_db):
    mongodb = MongoDB(collection_name='test_collection', db_name='test_db')
    db = mongodb.get_database()
    # Check if the database is created with the correct name
    assert db.name == mock_db['test_db'].name

def test_create_collection(mock_db):
    mongodb = MongoDB(collection_name='test_collection', db_name='test_db')
    collection = mongodb.create_collection('test_collection')
    # Check if the collection is created with the correct name
    assert collection.name == mock_db['test_db']['test_collection'].name

def test_insert_content(mock_db):
    mongodb = MongoDB(collection_name='test_collection', db_name='test_db')
    content = {"key": "value"}
    result = mongodb.insert_content(content)
    # Check if the content is inserted successfully
    assert result.acknowledged == True
  
def test_get_content(mock_db):
    mongodb = MongoDB(collection_name='test_collection', db_name='test_db')
    content = {"key": "value"}
    mongodb.insert_content(content)
    result = mongodb.get_content()
    # Remove the '_id' field from the result and content before comparing
    result.pop('_id', None)
    content.pop('_id', None)
    # Check if the content is retrieved successfully
    assert result == content