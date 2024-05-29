import re

import os
import sys

from pymongo.errors import DuplicateKeyError



sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.mongodb import MongoDB
from article_processor import ArticleProcessor



archive_db = MongoDB(db_name='archive', collection_name='archive_data')
cleaned_data_collection = MongoDB(db_name='clean_data', collection_name='slack_cleaned_data')
slack_original_data = MongoDB(db_name='slack_data', collection_name='amharic_news_data')


def main():
    text = "ጽኑ ህክምና የሚያስፈልጋ ቸው ሲሆኑ፤ ከዚህ ውስጥ ከ40 እስከ"
    columns_to_process = ['title']  # Add other columns to process here

    processor = ArticleProcessor(slack_original_data, cleaned_data_collection, archive_db, columns_to_process)
    processor.process_all_articles_in_collection()

if __name__ == '__main__':
    main()