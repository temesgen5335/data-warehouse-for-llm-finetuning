from enum import Enum
import json
import re
import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException



from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pprint import pprint

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import time
import platform

from rich.console import Console
from rich.table import Table
from rich.theme import Theme

# Create a logging custom theme
custom_theme = Theme({
    "success": "green",
    "info": "spring_green4"
})

# initialize the console with the custom theme
console = Console(theme=custom_theme, force_terminal=True)

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
        console.print(f"[success]Kafka producer initialized successfully[/success]")
        break
    except NoBrokersAvailable as e:
        print(f"An error occurred: {e}")
        if i < MAX_RETRIES - 1:  # No need to sleep on the last iteration
            time.sleep(RETRY_DELAY)
        else:
            raise  # Re-raise the last exception if all retries failed

class NewsCategory(Enum):
    POLITICS = 'politics'
    SOCIAL = 'social'
    ECONOMY = 'economy'
    VARIETIES = 'varities'
    SPORT = 'sports'



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

    def initialize_driver(self, category_page_url):
        for _ in range(3):  # retry up to 3 times
            try:
                self.driver.get(category_page_url)
                break  # if the navigation succeeds, break out of the loop
            except TimeoutException:
                print(f"Navigation timed out while trying to load {category_page_url}, retrying...")
        else:  # if the loop completes without breaking (i.e., all retries failed)
            print(f"Failed to load {category_page_url} after 3 attempts")
            # handle the failure (e.g., skip this page, raise an error, etc.)

    def get_all_articles(self):
        try:
            articles_elements = self.get_articles_element()
            return articles_elements
        except WebDriverException as e:
            print("Error occurred while retrieving the article elements:", e)
            raise
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
        except NoSuchElementException:
            return ""
        except WebDriverException as e:
            print(f"Error occurred while retrieving the image url of the article at {article.get('article_url')}: {str(e)}")
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
        
    def get_content_details(self):
        try:
            # Try to locate the element by id
            details_element = self.driver.find_element(By.ID, "content-details")
        except NoSuchElementException:
            try:
                # If locating the element by id fails, try to locate it by class name
                details_element = self.driver.find_element(By.CLASS_NAME, "details")
            except NoSuchElementException:
                print("Neither 'content-details' id nor 'details' class were found")
                return ""
        except Exception as e:
            print(f"An error occurred while locating the details element: {str(e)}")
            return ""

        return details_element.text

    def get_article_details(self, article_url, image_url, summary, category_value, title):
        # Navigate to the article URL
        self.driver.get(article_url)

        content = self.get_content_details()
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
            console.print("[info]Sent article to Kafka[/info]")

            # Close the current tab
            self.driver.close()

            # Switch back to the original tab
            self.driver.switch_to.window(self.driver.window_handles[0])

            return article_details
        except Exception as e:
            print(f"An error occurred while processing article on page {pages_to_scrape + 1} of category {category.value}: {e}")


    def read_last_scraped_page(self, category) -> int:
        try:
            with open(f'{category.value}_last_page.txt', 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def write_last_scraped_page(self, category, page_number):
        with open(f'{category.value}_last_page.txt', 'w') as f:
            f.write(str(page_number))

    def process_page(self, category, start_page):
        url = f'https://am.al-ain.com/section/{category.value}/page-{start_page}.html'
        self.initialize_driver(url)
        print("DRIVER INITIALIZED")

        from selenium.common.exceptions import NoSuchElementException
        successfully_scraped_urls = set()

        for i in range(3):  # Retry up to three times for the page
            try:
                articles = self.get_all_articles()
                if not articles:
                    print(f"No articles found on page {start_page} of category {category.value}")
                    break
                else:
                    for article in articles:
                        article_url = self.get_article_url(article)
                        if article_url in successfully_scraped_urls:
                            continue  # Skip this article if it has already been successfully scraped

                        for j in range(3):  # Retry up to three times for each article
                            try:
                                if article is not None and isinstance(article, WebElement):
                                    scraped_news_article = self.process_article(article, category, start_page - 1)
                                    console.print(f"[success]Success[/success]: {scraped_news_article.get('article_url')}")
                                    # print(f"Success: {scraped_news_article.get('article_url')}")
                                    successfully_scraped_urls.add(article_url)  # Add the URL of the successfully scraped article to the set
                                    break  # If the article was processed successfully, break out of the retry loop
                                else:
                                    print(f"Article on page {start_page} of category {category.value} is not an article WebElement")
                            except NoSuchElementException:
                                print("An error occurred while processing the article. Refreshing the article...")
                                self.driver.get(article_url)  # Navigate to the article's URL to refresh it
                                time.sleep(1)  # Wait for 1 second to allow the page to load
                                continue  # If a NoSuchElementException was raised, continue with the next retry
                            except Exception as e:
                                print(f"An error occurred while processing article on page {start_page} of category {category.value}: {str(e)}")
                                self.driver.get(article_url)  # Navigate to the article's URL to refresh it
                                time.sleep(1)  # Wait for 1 second to allow the page to load
                                continue  # If another exception was raised, continue with the next retry
            except NoSuchElementException:
                print("An error occurred while processing the page. Refreshing the page...")
                self.driver.refresh()
                continue  # If a NoSuchElementException was raised, continue with the next retry
            except Exception as e:
                print(f"An error occurred while processing page {start_page} of category {category.value}: {str(e)}")
                self.driver.refresh()
                continue  # If another exception was raised, continue with the next retry
            
    def scrape_news(self) -> list[dict]:
        print("Scraping News Started!!")
        news = []
        for page in range(1, self.number_of_pages_to_scrape + 1):
            print(f"Processing page {page}")
            for category in NewsCategory:
                print(category.value)
                last_scraped_page = self.read_last_scraped_page(category)

                # Check if this page has already been scraped for this category
                if page <= last_scraped_page:
                    print(f"Already scraped page {page} for category {category.value}")
                    continue

                self.process_page(category, page)

                # Write the last scraped page number to a file
                self.write_last_scraped_page(category, page)