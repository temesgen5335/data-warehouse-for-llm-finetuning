import faust

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database import MongoDB

from datetime import datetime
from models import ScrapedData

app = faust.App('myapp', broker='kafka://localhost:9092',)
scraped_data_topic = app.topic('scraped_data', value_type=ScrapedData)

# create a MongoDB instance
mongodb = MongoDB('bbc_news', 'scraped_data', 'mongodb://localhost:27018/')

@app.agent(scraped_data_topic)
async def process_data(scraped_data):
  async for data in scraped_data:
    # convert the title to uppercase
    data.url = data.url.upper()
    list_data = [data.to_dict()]

    mongodb.insert_content(data.to_dict())
    # print(type(data))

    print(list_data)

if __name__ == '__main__':
    app.main()