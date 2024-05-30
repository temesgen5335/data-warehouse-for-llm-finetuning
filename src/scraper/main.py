from news_scrapper import NewsScraper
import pprint
import time
from kafka.errors import NoBrokersAvailable

def hello():
    url = 'https://am.al-ain.com/'
    pages_to_scrape = 1000000
    scraper = NewsScraper(url=url, number_of_pages_to_scrape=pages_to_scrape)
    scraper.scrape_news()
        # pages_to_scrape += 1

        # for article in news:
        #     pprint.pprint(article)
        

if __name__ == "__main__":
    hello()