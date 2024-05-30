import pytest
from pymongo.errors import DuplicateKeyError
from mongomock import MongoClient

# import the MongoDB class from the database module
from src.database import MongoDB

# In your tests
class TestMongoDB:
    def setup_db(self):
        client = MongoClient()
        self.mongodb = MongoDB(client=client, collection_name='test_collection', db_name='test_db')

    def setup_method(self, method):
        self.setup_db()
        self.mongodb.collection.drop()

    def test_get_database(self):
        self.setup_method(None)
        db = self.mongodb.get_database()
        assert db.name == 'test_db'

    def test_create_collection(self):
        self.setup_method(None)
        collection = self.mongodb.create_collection('test_collection')
        # Check if the collection is created with the correct name
        assert collection.name == 'test_collection'

    def test_insert_content(self):
        self.setup_method(None)
        content = {"key": "value"}
        result = self.mongodb.insert_content(content)
        # Check if the content is inserted successfully
        assert result.acknowledged == True
    
    def test_get_content(self):
        self.setup_method(None)
        content = {"key": "value"}
        self.mongodb.insert_content(content)
        result = self.mongodb.get_content()
        # Remove the '_id' field from the result and content before comparing
        result.pop('_id', None)
        content.pop('_id', None)
        # Check if the content is retrieved successfully
        assert result == content

    def test_get_all_content(self):
        self.setup_method(None)
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

    def test_get_all_content_as_list(self):
        self.setup_method(None)
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

    def test_insert_many_content(self):
        self.setup_method(None)
        content = [{"key": "value1"}, {"key": "value2"}]
        result = self.mongodb.insert_many_content(content)
        # Check if the content is inserted successfully
        assert result.acknowledged == True

    def test_find_one(self):
        self.setup_method(None)
        content = {"key": "value"}
        self.mongodb.insert_content(content)
        result = self.mongodb.find_one()
        # Remove the '_id' field from the result and content before comparing
        result.pop('_id', None)
        content.pop('_id', None)
        # Check if the content is retrieved successfully
        assert result == content

    def test_delete_one(self):
        self.setup_method(None)
        content = {"key": "value"}
        self.mongodb.insert_content(content)
        # Pass a filter that matches the inserted document
        result = self.mongodb.delete_one(content)
        # Check if the content is deleted successfully
        assert result.deleted_count == 1

    def test_find(self):
        self.setup_method(None)
        content = [{"key": "value1"}, {"key": "value2"}]
        for c in content:
            self.mongodb.insert_content(c)
        results = list(self.mongodb.find())
        # Remove the '_id' field from the results and content before comparing
        for r in results:
            r.pop('_id', None)
        for c in content:
            c.pop('_id', None)
        
        # Check if all content is retrieved successfully
        assert results == content

    def test_save_content_to_txt(self):
        self.setup_method(None)
        content = [{"key": "value1"}, {"key": "value2"}]
        for c in content:
            self.mongodb.insert_content(c)
        fields = ['key']
        self.mongodb.save_content_to_txt(fields, output_file='output.txt')
        with open('output.txt', 'r') as f:
            lines = f.readlines()
        # Check if the content is saved to the output file successfully
        assert lines == ['value1\n', 'value2\n']

    def test_save_content_to_txt_with_many_fields(self):
        self.setup_method(None)
        content = [{"key1": "value1", "key2": "value2"}, {"key1": "value3", "key2": "value4"}]
        for c in content:
            self.mongodb.insert_content(c)
        fields = ['key1', 'key2']
        self.mongodb.save_content_to_txt(fields, output_file='output.txt')
        with open('output.txt', 'r') as f:
            lines = f.readlines()
        # Check if the content is saved to the output file successfully
        assert lines == ['value1 value2\n', 'value3 value4\n']