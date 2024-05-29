import re

import os
import sys

from pymongo.errors import DuplicateKeyError



sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.mongodb import MongoDB
from data_cleaning_utils import Normalize

archive_db = MongoDB(db_name='archive', collection_name='archive_data')
cleaned_data_collection = MongoDB(db_name='clean_data', collection_name='cleaned_data')
scraped_bbc = MongoDB(db_name='scraped_data', collection_name='bbc_news')


def process_text_and_display(text):
    # create an instance of the Normalize class
    normalizer = Normalize()

    # Test the function
    print("\nOriginal text: ")
    print(text)

    preprocessed_text = normalizer.clean_data(text)
    print("\n Preprocessed text:")
    print(preprocessed_text, "\n")

    print("==================Success==========================")


    return preprocessed_text




def process_article():
    print("Processing article...")

    # Fetch one article from the current database of unclean data
    article = scraped_bbc.find_one()

    # Save the _id of the article before processing it
    article_id = article['_id']

    # Process the article
    if article is not None:
        # Process the article
        clean_title = process_text_and_display(article.get('title'))

        # Update the article with the cleaned title
        article['title'] = clean_title

        try:
            # Try to save the processed article to the cleaned data database
            cleaned_data_collection.insert_content(article)
        except DuplicateKeyError:
            print(f"Article with _id {article['_id']} already exists in the cleaned_data collection.")

        # Delete the original article that has been processed from the scraped data database
        scraped_bbc.delete_one({'_id': article_id})

def process_all_articles_in_collection():
    print("Processing all articles in the collection...")

    # Fetch all articles from the current database of unclean data
    articles = scraped_bbc.find()

    # Process each article
    for article in articles:
        # Save the _id of the article before processing it
        article_id = article['_id']

        # Process the article
        if article is not None:
            # Process the article
            clean_title = process_text_and_display(article.get('title'))

            # Update the article with the cleaned title
            article['title'] = clean_title

            try:
                # Try to save the processed article to the cleaned data database
                cleaned_data_collection.insert_content(article)
            except DuplicateKeyError:
                print(f"Article with _id {article['_id']} already exists in the cleaned_data collection.")

            # Delete the original article that has been processed from the scraped data database
            scraped_bbc.delete_one({'_id': article_id})

    print("All articles have been processed.")


def main():
    text = "ጽኑ ህክምና የሚያስፈልጋቸው ሲሆኑ፤ ከዚህ ውስጥ ከ40 እስከ"
    clean_text = process_text_and_display(text)

    process_all_articles_in_collection()
    # process_article()

    # save the cleaned data to the database


if __name__ == '__main__':
    main()