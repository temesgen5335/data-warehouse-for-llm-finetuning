import re

import os
import sys

from pymongo.errors import DuplicateKeyError

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

os.chdir("../" )

from data_cleaning.data_cleaning_utils import Normalize


class ArticleProcessor:
  def __init__(self, scraped_collection=None, cleaned_collection=None, archive_collection=None, columns_to_process=[]):
    self.scraped_collection = scraped_collection
    self.cleaned_collection = cleaned_collection
    self.archive_collection = archive_collection
    self.columns_to_process = columns_to_process
    self.normalizer = Normalize()

  def process_text_and_display(self, text):
    # print("\nOriginal text: ")
    # print(text)

    preprocessed_text = self.normalizer.clean_data(text)
    # print("\n Preprocessed text:")
    # print(preprocessed_text, "\n")

    # print("==================Success==========================")

    return preprocessed_text

  def process_article(self, article):
    # Save the _id and url of the article before processing it
    article_id = article.get('_id')
    article_url = article.get('article_url')  # replace 'url' with your actual url field name

    # Process the article
    if article is not None:
      for column in self.columns_to_process:
        # Process the column
        clean_text = self.process_text_and_display(article.get(column))

        # Update the article with the cleaned text
        article[column] = clean_text

      if self.cleaned_collection is not None:
        # Prepare the query
        if article.get('_id'):
          query = {'$or': [{'article_url': article_url}, {'_id': article['_id']}]}
        else:
          query = {'article_url': article_url}

        # Check if the article with the same url or _id already exists
        existing_article = self.cleaned_collection.find_one(query)
        if existing_article:
          print(f"Article with url {article_url} or _id {article.get('_id')} already exists in the cleaned_data collection.")
        else:
          try:
            # Try to save the processed article to the cleaned data database
            self.cleaned_collection.insert_content(article)
          except DuplicateKeyError:
            print(f"Unexpected error: Article with _id {article.get('_id')} already exists in the cleaned_data collection.")

      if self.archive_collection is not None:
        # Move the original article to the archive database
        self.archive_collection.insert_content(article)

      if self.scraped_collection is not None:
        # Delete the original article that has been processed from the scraped data database
        self.scraped_collection.delete_one({'_id': article_id})

  def process_all_articles_in_collection(self):
    print("Processing all articles in the collection...")

    if self.scraped_collection is not None:
      # Fetch all articles from the current database of unclean data
      articles = self.scraped_collection.find()

      # Process each article
      for article in articles:
        self.process_article(article)

    print("All articles have been processed.")