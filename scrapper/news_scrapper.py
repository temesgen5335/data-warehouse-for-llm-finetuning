from enum import Enum
import os
import subprocess
import platform
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement

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
    LOADING = "ተጨማሪ ጫን"
    NEXT_PAGE = 'next page'

class NewsCollector:
    def __init__(self, url: str, headless: bool = True, pages_to_scrape: int = 1) -> None:
        self.setup_driver()
        options = Options()
        if headless:
            options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options, service=Service(executable_path=GECKODRIVER_PATH))
        self.url = url
        self.pages_to_scrape = pages_to_scrape

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
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except WebDriverException as e:
            raise

    def start_driver(self, category: NewsCategory) -> None:
        category_page_url = f"{self.url}/section/{category.value}/"
        try:
            self.driver.get(category_page_url)
        except WebDriverException as e:
            raise

    def get_articles_on_page(self) -> list[WebElement]:
        try:
            self.scroll_down()
            next_page = self.get_next_page()
            while next_page.text == NewsButton.LOADING.value:
                next_page = self.get_next_page()
            return self.get_articles()
        except WebDriverException as e:
            raise

    def get_articles(self) -> list[WebElement]:
        try:
            row_element = self.driver.find_element(By.XPATH, '//div[@class="row loadmore"]')
            articles = row_element.find_elements(By.TAG_NAME, 'article')
            return articles
        except WebDriverException as e:
            return []

    def get_next_page(self) -> WebElement:
        try:
            footer_element = self.driver.find_elements(By.TAG_NAME, 'footer')[0]
            return footer_element.find_element(By.TAG_NAME, 'a')
        except WebDriverException as e:
            raise

    def get_image(self, article: WebElement) -> str:
        try:
            image_element = article.find_element(By.TAG_NAME, 'img')
            image_url = image_element.get_attribute('srcset')
            image_url = re.sub(r'\s\d+w', '', image_url).split(',')[0]
            return image_url.strip()
        except WebDriverException as e:
            return ""

    def get_headline(self, article: WebElement) -> str:
        try:
            title_element = article.find_element(By.CLASS_NAME, 'card-title').find_element(By.TAG_NAME, 'a')
            return title_element.text
        except WebDriverException as e:
            return ""

    def get_article_link(self, article: WebElement) -> str:
        try:
            title_element = article.find_element(By.CLASS_NAME, 'card-title').find_element(By.TAG_NAME, 'a')
            return title_element.get_attribute('href')
        except WebDriverException as e:
            return ""

    def get_summary(self, article: WebElement) -> str:
        try:
            highlight_element = article.find_element(By.CLASS_NAME, 'card-text')
            return highlight_element.text
        except WebDriverException as e:
            return ""

    def get_publish_time(self, article: WebElement) -> str:
        try:
            time_element = article.find_element(By.TAG_NAME, 'time')
            return time_element.text
        except WebDriverException as e:
            return ""

    def collect_news(self) -> list[dict]:
        news = []
        for category in NewsCategory:
            self.start_driver(category)
            pages_to_scrape = self.pages_to_scrape
            while pages_to_scrape > 0:
                pages_to_scrape -= 1
                articles = self.get_articles_on_page()
                if articles:
                    for article in articles:
                        try:
                            news.append(
                                {
                                    "image_url": self.get_image(article),
                                    "title": self.get_headline(article),
                                    "article_url": self.get_article_link(article),
                                    "highlight": self.get_summary(article),
                                    "time_publish": self.get_publish_time(article),
                                    "category": category.value
                                }
                            )
                        except (WebDriverException, AttributeError, Exception) as e:
                            print(e)
        return news
    ...
    def exit_driver(self) -> None:
        try:
            self.driver.quit()
        except WebDriverException as e:
            print("WebDriverException error occurred while quitting the driver:", e)
            raise