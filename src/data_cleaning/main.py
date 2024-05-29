import re

import os
import sys

from pymongo.errors import DuplicateKeyError



sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.mongodb import MongoDB
from article_processor import ArticleProcessor



archive_db = MongoDB(db_name='archive', collection_name='kaggle_amharic_corpus')
cleaned_data_collection = MongoDB(db_name='clean_data', collection_name='kaggle_amharic_corpus_cleaned')

# The collection with unclean data
original_data_collection = MongoDB(db_name='kaggle_data', collection_name='amharic_corpus_merged')


def main():
    text = "ጽኑ ህክምና የሚያስፈልጋ ቸው ሲሆኑ፤ ከዚህ ውስጥ ከ40 እስከ"
    columns_to_process = ['content']  # Add other columns to process here

    processor = ArticleProcessor(original_data_collection, cleaned_data_collection, archive_db, columns_to_process)
    processor.process_all_articles_in_collection()

if __name__ == '__main__':
    main()