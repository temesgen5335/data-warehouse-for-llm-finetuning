from news_scrapper import NewsScraper
import pprint
import time
from kafka.errors import NoBrokersAvailable

def main():
    url = 'https://am.al-ain.com/'
    pages_to_scrape = 1000
    scraper = NewsScraper(url=url, number_of_pages_to_scrape=pages_to_scrape)
    scraper.scrape_news()

    while True:
        try:
            scraper.scrape_news()
            break  # If scrape_news completes successfully, break the loop
        except Exception as e:  # Replace Exception with the specific exception you're handling
            print(f"Error occurred: {e}. Retrying...")
            time.sleep(3)  # Wait for 3 seconds before retrying
        

if __name__ == "__main__":
    main()