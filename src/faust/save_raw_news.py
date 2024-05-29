import faust
import os

from database import MongoDB

from datetime import datetime
from models import ScrapedNews

# Load the environment variables from the .env file
from dotenv import load_dotenv

KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', 'kafka://localhost:9094')
MONGODB_CONNECTION_STRING = os.getenv('MONGODB_CONNECTION_STRING', 'mongodb://localhost:27017/')

app = faust.App('myapp', broker=KAFKA_BROKER_URL)
scraped_data_topic = app.topic('scraping', value_type=ScrapedNews)

# create a MongoDB instance (for saving the data after processing)
mongodb = MongoDB('bbc_news', 'scraped_data', MONGODB_CONNECTION_STRING)


@app.agent(scraped_data_topic)
async def save_raw_news(scraped_data):
  async for data in scraped_data:
    # HERE WE PREPROCESS THE DATA
    # For now we'll just convert the title to uppercase

    # convert the title to uppercase
    data.article_url = data.article_url.upper()
    
    data = data.asdict()

    # Save the data to MongoDB
    # mongodb.insert_content(data.to_dict())

    print(type(data))
    print(data.get("article_url"))
    # print(data.article_url)


if __name__ == '__main__':
    app.main()