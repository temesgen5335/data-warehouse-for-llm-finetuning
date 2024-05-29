import pandas as pd

from pymongo import MongoClient
from mongodb import MongoDB

import os
import sys

# sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the path to the CSV file
csv_path = os.path.join(script_dir, '../../data/slack/Amharic_News_Dataset.csv')

def load_data_to_mongo():
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path)
    
    # Rename the columns
    columns_to_rename = {
        'headline': 'title',
        'date': 'published_date',
        'article': 'content',
        'category': 'category',
        'link': 'article_url'
    }

    df.rename(columns=columns_to_rename, inplace=True)

    # Create a MongoDB object
    mongodb = MongoDB(collection_name='amharic_news_data', db_name='slack_data')

    # Insert the data into MongoDB
    mongodb.insert_many_content(df.to_dict('records'))

    print("Loading data...")

def main():
    # load_data_to_mongo()
    load_data_to_mongo()

if __name__ == '__main__':
    main()