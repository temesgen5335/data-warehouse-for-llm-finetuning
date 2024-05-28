from news_scrapper import NewsScraper

def main():
    url = 'https://am.al-ain.com/'
    pages_to_scrape = 2
    try:
        scraper = NewsScraper(url=url, number_of_pages_to_scrape=pages_to_scrape)
        news_data = scraper.get_full_news()

        # print(news_data)
        print(news_data[0])
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()