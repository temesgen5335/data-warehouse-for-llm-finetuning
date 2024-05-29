from news_scrapper import NewsScraper, NewsCategory
import pprint

def hello():
    url = 'https://am.al-ain.com/'
    pages_to_scrape = 2
    try:
        print("Scraping started ")

        scraper = NewsScraper(url, pages_to_scrape)
        # Initialize the scraper for a specific category
        # scraper.initialize_driver(NewsCategory.POLITICS)
        news = scraper.scrape_news()
        for article in news:
            pprint(article)

        # Get the next article value
        # article = sc.get_next_article_value()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    hello()