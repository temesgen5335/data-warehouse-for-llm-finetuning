from enum import Enum
import json
import re
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pprint import pprint

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import time
import platform
# import logging
# import sys
# 
# logging.basicConfig(level=logging.INFO, stream=sys.stdout)


GECKODRIVER_VERSION = '0.34.0'
GECKODRIVER_PATH = './geckodriver'
PLATFORM_ARCHITECTURE = platform.machine()
GECKODRIVER_FOLDER = './geckodriver'


KAFKA_TOPIC = 'scraping'
KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'
MAX_RETRIES = 5
RETRY_DELAY = 2  # delay between retries in seconds

producer = None
for i in range(MAX_RETRIES):
    try:
        producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        # If the initialization is successful, break from the loop
        break
    except NoBrokersAvailable as e:
        print(f"An error occurred: {e}")
        if i < MAX_RETRIES - 1:  # No need to sleep on the last iteration
            time.sleep(RETRY_DELAY)
        else:
            raise  # Re-raise the last exception if all retries failed

class NewsCategory(Enum):
    POLITICS = 'politics'
    # SOCIAL = 'social'
    # ECONOMY = 'economy'
    # VARIETIES = 'varities'
    # SPORT = 'sports'



class NewsButton(Enum):
    LOADING = "ተጨማሪ ጫን"
    NEXT_PAGE = 'next page'


class NewsScraper:
    def __init__(self, url: str, headless: bool = True, number_of_pages_to_scrape: int = 2) -> None:
        self.setup_driver()
        options = Options()
        if headless:
            options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options, service=Service(executable_path=GECKODRIVER_PATH))
        self.url = url
        self.number_of_pages_to_scrape = number_of_pages_to_scrape

    # TODO - Add error handling
    def setup_driver(self, version=GECKODRIVER_VERSION):
            if not os.path.exists(GECKODRIVER_PATH):
                PLATFORM_ARCHITECTURE = platform.machine()

                if PLATFORM_ARCHITECTURE == 'aarch64':
                    geckofile_type = 'linux-aarch64'
                elif PLATFORM_ARCHITECTURE == 'x86_64':
                    geckofile_type = 'linux64'
                else:
                    raise ValueError(f'Unsupported architecture: {PLATFORM_ARCHITECTURE}')

                subprocess.run(['wget', '-q', f'https://github.com/mozilla/geckodriver/releases/download/v{version}/geckodriver-v{version}-{geckofile_type}.tar.gz'])
                GECKODRIVER_TAR_FILE_PATH = f'./geckodriver-v{version}-{geckofile_type}.tar.gz'

                subprocess.run(['tar', '-xzf', GECKODRIVER_TAR_FILE_PATH])
                subprocess.run(['rm', GECKODRIVER_TAR_FILE_PATH])
                subprocess.run(['chmod', '+x', GECKODRIVER_PATH])


    def scroll_to_bottom(self) -> None:
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except WebDriverException as e:
            print("Error occurred while scrolling to the bottom of the page:", e)
            raise

    def initialize_driver(self, category_page_url) -> None:

        try:
            self.driver.get(category_page_url)
            print(category_page_url)
        except WebDriverException as e:
            print("Error occurred while navigating to the category page:", e)
            raise


    def get_all_articles(self) -> list[WebElement]:
        articles = []
        try:
            self.scroll_to_bottom()
        except WebDriverException as e:
            print("Error occurred while scrolling to the bottom of the page:", e)
            raise

        next_page = self.get_next_page_element()
        while next_page.text == NewsButton.LOADING.value:
            try:
                next_page = self.get_next_page_element()
            except WebDriverException as e:
                print("Error occurred while waiting for the next page element to load:", e)
                raise

        articles_elements = self.get_articles_element()
        for article in articles_elements:
            articles.append(article)

        return articles
        ...

    def get_next_article(self) -> WebElement:
        try:
            self.scroll_to_bottom()
        except WebDriverException as e:
            print("Error occurred while scrolling to the bottom of the page:", e)
            raise

        next_page = self.get_next_page_element()
        while next_page.text == NewsButton.LOADING.value:
            try:
                next_page = self.get_next_page_element()
            except WebDriverException as e:
                print("Error occurred while waiting for the next page element to load:", e)
                raise

        try:
            articles = self.get_articles_element()
            if articles:
                return articles.pop(0)
            else:
                return None
        except WebDriverException as e:
            print("Error occurred while retrieving the article elements:", e)
            raise

    def has_next_article(self) -> bool:
        try:
            articles = self.get_articles_element()
            return bool(articles)
        except WebDriverException as e:
            print("Error occurred while checking for more articles:", e)
            return False

    def get_next_article_value(self) -> dict:
        article = self.get_next_article()
        if article is None:
            return None

        try:
            return {
                "image_url": self.get_image_url(article),
                "title": self.get_title(article),
                "article_url": self.get_article_url(article),
                "summary": self.get_summary(article),
                "category": category.value
            }
        except (WebDriverException, AttributeError, Exception) as e:
            print(f"An error occurred while scraping article:", e)
            return None

    def get_articles_element(self) -> list[WebElement]:
        try:
            row_element = self.driver.find_element(By.XPATH, '//div[@class="row loadmore"]')
            articles = row_element.find_elements(By.TAG_NAME, 'article')
            if not articles:
                print("No articles found on the page.")
            return articles
        except WebDriverException as e:
            print("Error occurred while retrieving the article elements:", e)
            return []

    def get_next_page_element(self) -> WebElement:
        try:
            footer_element = self.driver.find_elements(By.TAG_NAME, 'footer')[0]
            return footer_element.find_element(By.TAG_NAME, 'a')
        except WebDriverException as e:
            print("Error occurred while retrieving the next page element:", e)
            raise

    def get_image_url(self, article: WebElement) -> str:
        try:
            image_element = article.find_element(By.TAG_NAME, 'img')
            image_url = image_element.get_attribute('srcset')
            image_url = re.sub(r'\s\d+w', '', image_url).split(',')[0]
            return image_url.strip()
        except WebDriverException as e:
            print("Error occurred while retrieving the image url of the article:", e)
            return ""

    def get_title(self, article: WebElement) -> str:
        try:
            title_element = article.find_element(By.CLASS_NAME, 'card-title').find_element(By.TAG_NAME, 'a')
            return title_element.text
        except WebDriverException as e:
            print("Error occurred while retrieving the title of the article:", e)
            return ""

    def get_article_url(self, article: WebElement) -> str:
        try:
            title_element = article.find_element(By.CLASS_NAME, 'card-title')
            link_element = title_element.find_element(By.TAG_NAME, 'a')
            return link_element.get_attribute('href')
        except WebDriverException as e:
            print("Error occurred while retrieving the article url of the article:", e)
            return ""

    def get_summary(self, article: WebElement) -> str:
        try:
            highlight_element = article.find_element(By.CLASS_NAME, 'card-text')
            return highlight_element.text
        except WebDriverException as e:
            print("Error occurred while retrieving the highlight of the article:", e)
            return ""

    def get_time_publish(self, article: WebElement) -> str:
        try:
            time_element = article.find_element(By.TAG_NAME, 'time')
            return time_element.text
        except WebDriverException as e:
            print("Error occurred while retrieving the time publish of the article:", e)
            return ""

    def get_article_details(self, article_url, image_url, summary, category_value, title):
        # Navigate to the article URL
        self.driver.get(article_url)

        content = self.driver.find_element(By.ID, 'content-details').text
        published_date = self.driver.find_element(By.CLASS_NAME, 'tags').find_element(By.TAG_NAME, 'time').text
        author = self.driver.find_element(By.CLASS_NAME, 'card-author').text

        return {
            "image_url": image_url,
            "title": title,
            "article_url": article_url,
            "summary": summary,
            "category": category_value,
            "content": content,
            "author": author,
            "source": self.url,
            "published_date": published_date
        }

    def process_article(self, article, category, pages_to_scrape):
        try:
            # Extract all details BEFORE navigating to the article page
            image_url = self.get_image_url(article)
            title = self.get_title(article)
            article_url = self.get_article_url(article)
            summary = self.get_summary(article)

            # Open a new tab
            self.driver.execute_script("window.open();")

            # Switch to the new tab (it's always the last one)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            article_details = self.get_article_details(
                article_url, image_url, summary, category.value, title
            )

            # Send the article to a Kafka topic in Kafka, for further processing
            producer.send(KAFKA_TOPIC, article_details)
            print(f"Sent article to Kafka: {article_details.get('article_url')}")

            # Close the current tab
            self.driver.close()

            # Switch back to the original tab
            self.driver.switch_to.window(self.driver.window_handles[0])

            return article_details
        except Exception as e:
            print(f"An error occurred while processing article on page {pages_to_scrape + 1} of category {category.value}: {e}")



    def scrape_news(self) -> list[dict]:
        print("Scraping News Started!!")
        news = []
        for category in NewsCategory:
            print(category.value)
            # Read the last scraped page number from a file
            try:
                with open(f'{category.value}_last_page.txt', 'r') as f:
                    start_page = int(f.read().strip())
            except (FileNotFoundError, ValueError):
                start_page = 0

            # Check if the number of pages to scrape has already been reached
            if start_page >= self.number_of_pages_to_scrape:
                print(f"Already scraped {self.number_of_pages_to_scrape} pages for category {category.value}")
                continue

            pages_to_scrape = self.number_of_pages_to_scrape - start_page
            
            while pages_to_scrape > 0:
                pages_to_scrape -= 1
                start_page += 1  # Increment the page number
                print("START PAGE: ", start_page)
                print("PAGE TO SCRAPE: ", pages_to_scrape)

                # Modify the URL based on the current page number
                url = f'https://am.al-ain.com/section/{category.value}/page-{start_page}.html'
                self.initialize_driver(url)
                print("DRIVER INITIALIZED")

                articles = self.get_all_articles()

                first_articles = articles[:2]

                if not articles:
                    print(f"No articles found on page {start_page} of category {category.value}")
                    break
                else:
                    for article in first_articles:
                        scraped_news_article = self.process_article(article, category, start_page - 1)
                        print(f"Success: {scraped_news_article.get('article_url')}")

                    # Write the last scraped page number to a file
                    with open(f'{category.value}_last_page.txt', 'w') as f:
                        f.write(str(start_page))
    