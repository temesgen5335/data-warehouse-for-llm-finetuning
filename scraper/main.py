from news_scrapper import NewsCollector

def main():
    url = 'https://am.al-ain.com/'
    pages_to_scrape = 2
    try:
        scraper = NewsCollector(url=url, pages_to_scrape=pages_to_scrape)
        news_data = scraper.collect_all_news_content()

        print(news_data)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()