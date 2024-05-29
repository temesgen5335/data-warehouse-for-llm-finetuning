import faust
import os
import sys

from database import MongoDB

from datetime import datetime
from models import ScrapedNews

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# os.chdir("../")

print(os.getcwd())

from data_cleaning.article_processor import ArticleProcessor

# Load the environment variables from the .env file
from dotenv import load_dotenv

KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', 'kafka://localhost:9094')
MONGODB_CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING', 'mongodb://localhost:27017/')

app = faust.App('myapp', broker=KAFKA_BROKER_URL)
scraped_data_topic = app.topic('scraping', value_type=ScrapedNews)

# create a MongoDB instance (for saving the data after processing)
mongodb = MongoDB('alain_news', 'scraped_data', MONGODB_CONNECTION_STRING)



@app.agent(scraped_data_topic)
async def save_raw_news(scraped_data):
  # Initialize the ArticleProcessor
  processor = ArticleProcessor(columns_to_process=['article_url'])

  async for data in scraped_data:
    # Convert the data to a dictionary
    data_dict = data.asdict()

    # Check if data_dict is not None before processing it
    if data_dict is not None:
      # Process the data using the ArticleProcessor
      processed_data = processor.process_article(data_dict)

      # Check if processed_data is not None before saving it to MongoDB
      if processed_data is not None:
        # Save the processed data to MongoDB
        # mongodb.insert_content(processed_data)

        print(type(processed_data))
        print(processed_data.get("article_url"))

if __name__ == '__main__':
    app.main()