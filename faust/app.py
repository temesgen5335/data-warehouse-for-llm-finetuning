import faust
import os

from database import MongoDB

from datetime import datetime
from models import ScrapedData

KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL', 'kafka://localhost:9093')
<<<<<<< HEAD
MONGODB_CONNECTION_STRING = 'mongodb://mongodb:27017/'

=======

MONGODB_CONNECTION_STRING = 'mongodb://mongodb:27017/'

>>>>>>> 6487848afdaca29a4493f7ccf256000a652acc22
app = faust.App('myapp', broker=KAFKA_BROKER_URL)
scraped_data_topic = app.topic('scraped_data', value_type=ScrapedData)

# create a MongoDB instance (for saving the data after processing)
mongodb = MongoDB('bbc_news', 'scraped_data', MONGODB_CONNECTION_STRING)

@app.agent(scraped_data_topic)
async def process_data(scraped_data):
  async for data in scraped_data:
    # HERE WE PREPROCESS THE DATA
    # For now we'll just convert the title to uppercase

    # convert the title to uppercase
    data.url = data.url.upper()
    list_data = [data.to_dict()]

    # Save the data to MongoDB
    mongodb.insert_content(data.to_dict())
    # print(type(data))

    print(list_data)

if __name__ == '__main__':
    app.main()