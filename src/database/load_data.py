import pandas as pd

from pymongo import MongoClient
from mongodb import MongoDB

import os
import sys

# sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

# Get the directory of the current script
# script_dir = os.path.dirname(__file__)

# Construct the path to the CSV file
# csv_path = os.path.join(script_dir, '../../data/slack/Amharic_News_Dataset.csv')


def load_data_to_mongo(csv_file_path, columns_to_rename, source, db_name, collection_name):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Rename the columns
    df.rename(columns=columns_to_rename, inplace=True)

    # Add source column and set it to the provided source
    df['source'] = source

    # Create a MongoDB object with the provided database and collection names
    mongodb = MongoDB(collection_name=collection_name, db_name=db_name)

    # Insert the data into MongoDB
    mongodb.insert_many_content(df.to_dict('records'))

    print(f"Data from {csv_file_path} loaded successfully!")


def main():
    def main():
        data_files = [
            {
                'csv_file_path': '../data/slack/Amharic_News_Dataset.csv',
                'columns_to_rename': {
                    'headline': 'title',
                    'date': 'published_date',
                    'article': 'content',
                    'category': 'category',
                    'link': 'article_url',
                },
                'source': 'slack',
                'db_name': 'slack_data',
                'collection_name': 'amharic_news_data',
            },
            # Add more dictionaries here for other CSV files
        ]

        for data_file in data_files:
            load_data_to_mongo(**data_file)
        
    if __name__ == '__main__':
        main()

if __name__ == '__main__':
    main()