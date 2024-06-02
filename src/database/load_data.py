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
    # Get the absolute path to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the CSV file
    csv_file_path = os.path.join(script_dir, csv_file_path)

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

    # Write the name of the processed file to the log file
    with open('processed_files.log', 'a') as f:
        f.write(csv_file_path + '\n')

    # Return the absolute path of the CSV file
    return csv_file_path

def main():
    # Load the names of the processed files into a set
    with open('processed_files.log', 'a+') as f:
        f.seek(0)
        processed_files = set(line.strip() for line in f)


    data_files = [
        {
            'csv_file_path': '../../data/slack/Amharic_News_Dataset.csv',
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
        {
            'csv_file_path': '../../data/kaggle/Amharic_corpus_merged_2023-04-16.csv',
            'columns_to_rename': {
                'article': 'content'
            },
            'source': 'kaggle',
            'db_name': 'kaggle_data',
            'collection_name': 'amharic_corpus_merged',
        }
        # add more dictionaries for other data files to save here
    ]

    for data_file in data_files:
        # Get the absolute path of the CSV file
        csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), data_file['csv_file_path'])

        # Skip the file if it has already been processed
        if csv_file_path in processed_files:
            print(f"Skipping {csv_file_path} (already processed)")
            continue

        load_data_to_mongo(**data_file)

if __name__ == '__main__':
    main()