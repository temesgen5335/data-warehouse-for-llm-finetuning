from enum import Enum
import os
import subprocess
import platform
import re
import platform
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.chdir('./')

GECKODRIVER_VERSION = '0.34.0'
GECKODRIVER_PATH = './geckodriver'
PLATFORM_ARCHITECTURE = platform.machine()
GECKODRIVER_FOLDER = './geckodriver'

class NewsCategory(Enum):
    POLITICS = 'politics'
    SOCIAL = 'social'
    ECONOMY = 'economy'
    VARIETIES = 'varities'
    SPORT = 'sports'

class NewsButton(Enum):
class NewsButton(Enum):
    LOADING = "ተጨማሪ ጫን"
    NEXT_PAGE = 'next page'

class NewsCollector:
    def __init__(self, url: str, headless: bool = True, pages_to_scrape: int = 1) -> None:
        self.setup_driver()
class NewsCollector:
    def __init__(self, url: str, headless: bool = True, pages_to_scrape: int = 1) -> None:
        self.setup_driver()
        options = Options()
        if headless:
            options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options, service=Service(executable_path=GECKODRIVER_PATH))
        self.driver = webdriver.Firefox(options=options, service=Service(executable_path=GECKODRIVER_PATH))
        self.url = url
        self.pages_to_scrape = pages_to_scrape

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

    def scroll_down(self) -> None:
        # sets the scroll position to the max height of the document body
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except WebDriverException as e:
            raise

    def start_driver(self, category: NewsCategory) -> None:
        # goes to the category page given in the parameter
        category_page_url = f"{self.url}/section/{category.value}/"
        try:
            self.driver.get(category_page_url)
        except WebDriverException as e:
            raise

    def get_articles_on_page(self) -> list[WebElement]:
        # Scrolls down to the bottom of the page to load all articles, if any
        #  gets the next page element of checks if it is still loading
        # Returns a list of articles on the page of the given category
        try:
            self.scroll_down()
            next_page = self.get_next_page()
            while next_page.text == NewsButton.LOADING.value:
                next_page = self.get_next_page()
            return self.get_articles()
        except WebDriverException as e:
            raise

    def get_articles(self) -> list[WebElement]:
    def get_articles(self) -> list[WebElement]:
        try:
            row_element = self.driver.find_element(By.XPATH, '//div[@class="row loadmore"]')
            articles = row_element.find_elements(By.TAG_NAME, 'article')
            return articles
        except WebDriverException as e:
            return []

    def get_next_page(self) -> WebElement:
    def get_next_page(self) -> WebElement:
        try:
            footer_element = self.driver.find_elements(By.TAG_NAME, 'footer')[0]
            return footer_element.find_element(By.TAG_NAME, 'a')
        except WebDriverException as e:
            raise

    def get_image(self, article: WebElement) -> str:
    def get_image(self, article: WebElement) -> str:
        try:
            image_element = article.find_element(By.TAG_NAME, 'img')
            image_url = image_element.get_attribute('srcset')
            image_url = re.sub(r'\s\d+w', '', image_url).split(',')[0]
            return image_url.strip()
        except WebDriverException as e:
            return ""

    def get_headline(self, article: WebElement) -> str:
    def get_headline(self, article: WebElement) -> str:
        try:
            title_element = article.find_element(By.CLASS_NAME, 'card-title').find_element(By.TAG_NAME, 'a')
            return title_element.text
        except WebDriverException as e:
            return ""

    def get_article_link(self, article: WebElement) -> str:
    def get_article_link(self, article: WebElement) -> str:
        try:
            title_element = article.find_element(By.CLASS_NAME, 'card-title').find_element(By.TAG_NAME, 'a')
            return title_element.get_attribute('href')
        except WebDriverException as e:
            return ""

    def get_summary(self, article: WebElement) -> str:
    def get_summary(self, article: WebElement) -> str:
        try:
            highlight_element = article.find_element(By.CLASS_NAME, 'card-text')
            return highlight_element.text
        except WebDriverException as e:
            return ""

    def get_publish_time(self, article: WebElement) -> str:
    def get_publish_time(self, article: WebElement) -> str:
        try:
            time_element = article.find_element(By.TAG_NAME, 'time')
            return time_element.text
        except WebDriverException as e:
            return ""

    def get_word_count(self, text: str) -> int:
        return len(text.split())

    def get_language(self) -> str:
        return 'am'

    def collect_all_news_content(self) -> list[dict]:
        """
        Collects full news articles by scraping the content pages of each article.

        Returns:
            list[dict]: A list of dictionaries containing information about each full news article.
        """
        news = self.collect_news()  # Collect the news articles
        for article in news:
            try:
                # Navigate to the article page
                self.driver.get(article.get('article_url'))

                article["published_date"] = self.driver.find_element(By.CLASS_NAME, 'tags').find_element(By.TAG_NAME, 'time').text
                article["author"] = self.driver.find_element(By.CLASS_NAME, 'card-author').text
                article["content"] = self.driver.find_element(By.ID, 'content-details').text
            except (WebDriverException, AttributeError, Exception) as e:
                print(f"An error occurred while scraping content page of category {article['category']} and url {article['article_url']}: {e}")
        return news

    def collect_news(self) -> list[dict]:
        """
        Collects news articles from different categories and returns a list of dictionaries.

        Returns:
            list[dict]: A list of dictionaries containing information about each news article.
        """
        news = []  # List to store the collected news articles

        # Iterate over each category
        for category in NewsCategory:
            self.start_driver(category)  # Start the web driver for the current category
            pages_to_scrape = self.pages_to_scrape  # Get the number of pages to scrape for the current category

            # Scrape the specified number of pages
            while pages_to_scrape > 0:
                pages_to_scrape -= 1
                articles = self.get_articles_on_page()  # Get the articles on the current page

                if articles:
                    # Process each article and add it to the news list
                    for article in articles:
                        try:
                            news.append(
                                {
                                    "image_url": self.get_image(article),
                                    "title": self.get_headline(article),
                                    "article_url": self.get_article_link(article),
                                    "summary": self.get_summary(article),
                                    "published_date": self.get_publish_time(article),
                                    "language": self.get_language(),
                                    "category": category.value
                                }
                            )
                        except (WebDriverException, AttributeError, Exception) as e:
                            print(e)

                # Get the next page element
                next_page = self.get_next_page()

                # Check if the next page element is the "Next Page" button and there are more pages to scrape
                if next_page.text == NewsButton.NEXT_PAGE.value and pages_to_scrape > 0:
                    # Click the next page element
                    self.driver.execute_script("arguments[0].click();", next_page)
                else:
                    # Stop scraping if there are no more pages or the next page element is not the "Next Page" button
                    break

        return news

