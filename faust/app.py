import faust

from datetime import datetime
from models import ScrapedData

app = faust.App('myapp', broker='kafka://localhost:9092',)
topic = app.topic('scraped_data', value_type=ScrapedData)

@app.agent(topic)
async def process_data(scraped_data):
  async for data in scraped_data:
    # convert the title to uppercase
    data.url = data.url.upper()

    print(data)

if __name__ == '__main__':
    app.main()