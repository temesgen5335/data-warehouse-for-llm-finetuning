import re

import os
import sys

from pymongo.errors import DuplicateKeyError

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from data_cleaning_utils import Normalize


class ArticleProcessor:
  def __init__(self, scraped_collection, cleaned_collection, archive_collection, columns_to_process):
    self.scraped_collection = scraped_collection
    self.cleaned_collection = cleaned_collection
    self.archive_collection = archive_collection
    self.columns_to_process = columns_to_process
    self.normalizer = Normalize()

  def process_text_and_display(self, text):
    print("\nOriginal text: ")
    print(text)

    preprocessed_text = self.normalizer.clean_data(text)
    print("\n Preprocessed text:")
    print(preprocessed_text, "\n")

    print("==================Success==========================")

    return preprocessed_text

  def process_article(self, article):
    # Save the _id of the article before processing it
    article_id = article['_id']

    # Process the article
    if article is not None:
      for column in self.columns_to_process:
        # Process the column
        clean_text = self.process_text_and_display(article.get(column))

        # Update the article with the cleaned text
        article[column] = clean_text

      try:
        # Try to save the processed article to the cleaned data database
        self.cleaned_collection.insert_content(article)
      except DuplicateKeyError:
        print(f"Article with _id {article['_id']} already exists in the cleaned_data collection.")

      # Move the original article to the archive database
      self.archive_collection.insert_content(article)

      # Delete the original article that has been processed from the scraped data database
      self.scraped_collection.delete_one({'_id': article_id})

  def process_all_articles_in_collection(self):
    print("Processing all articles in the collection...")

    # Fetch all articles from the current database of unclean data
    articles = self.scraped_collection.find()

    # Process each article
    for article in articles:
      self.process_article(article)

    print("All articles have been processed.")