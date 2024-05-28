from enum import Enum
import re
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException

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
    def __init__(
            self,
            url: str,
            headless: bool = True,
            number_of_pages_to_scrape: int = 1
    ) -> None:
        self.setup_geckodriver()
        options = Options()
        if headless:
            options.add_argument("--headless")
        self.driver = webdriver.Firefox(
            options=options,
            service=Service(executable_path='./geckodriver')
        )
        self.url = url
        self.number_of_pages_to_scrape = number_of_pages_to_scrape


    def setup_geckodriver(self, version='0.34.0'):
        if not os.path.exists('./geckodriver'):
            download = subprocess.run(['wget', '-q',
                                       f'https://github.com/mozilla/geckodriver/releases/download/v{version}/geckodriver-v{version}-linux-aarch64.tar.gz'])
            if download.returncode != 0:
                print("Failed to download geckodriver")
                return
            extract = subprocess.run(['tar', '-xzf', f'geckodriver-v{version}-linux-aarch64.tar.gz'])
            if extract.returncode != 0:
                print("Failed to extract geckodriver")
                return
            subprocess.run(['rm', f'geckodriver-v{version}-linux-aarch64.tar.gz'])
            chmod = subprocess.run(['chmod', '+x', './geckodriver'])
            if chmod.returncode != 0:
                print("Failed to change permissions of geckodriver")



    def scroll_to_bottom(self) -> None:
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except WebDriverException as e:
            print("Error occurred while scrolling to the bottom of the page:", e)
            raise

    def initialize_driver(self, category: NewsCategory) -> None:
        category_page_url = f"{self.url}/section/{category.value}/"

        try:
            self.driver.get(category_page_url)
        except WebDriverException as e:
            print("Error occurred while navigating to the category page:", e)
            raise

    def get_all_articles(self) -> list[WebElement]:
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
            return self.get_articles_element()
        except WebDriverException as e:
            print("Error occurred while retrieving the article elements:", e)
            raise

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
            title_element = article.find_element(By.CLASS_NAME, 'card-title').find_element(By.TAG_NAME, 'a')
            return title_element.get_attribute('href')
        except WebDriverException as e:
            print("Error occurred while retrieving the article url of the article:", e)
            return ""

    def get_highlight(self, article: WebElement) -> str:
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

    def get_news(self) -> list[dict]:
        news = []
        for category in NewsCategory:
            self.initialize_driver(category)
            pages_to_scrape = self.number_of_pages_to_scrape
            while pages_to_scrape > 0:
                pages_to_scrape -= 1
                articles = self.get_all_articles()
                if not articles:
                    print(f"No articles found on page {pages_to_scrape + 1} of category {category.value}")
                else:
                    for article in articles:
                        try:
                            news.append(
                                {
                                    "image_url": self.get_image_url(article),
                                    "title": self.get_title(article),
                                    "article_url": self.get_article_url(article),
                                    "highlight": self.get_highlight(article),
                                    "category": category.value
                                }
                            )
                        except (WebDriverException, AttributeError, Exception) as e:
                            print(f"An error occurred while scraping article on page {pages_to_scrape + 1} of category {category.value}:", e)
                next_page = self.get_next_page_element()
                if next_page.text == NewsButton.NEXT_PAGE.value and pages_to_scrape > 0:
                    self.driver.execute_script("arguments[0].click();", next_page)
                else:
                    break
        return news

    def get_full_news(self) -> list[dict]:
        news = self.get_news()
        for n in news:
            try:
                self.driver.get(n.get('article_url'))
                detail_content = self.driver.find_element(By.ID, 'content-details').text
                publisher_name = self.driver.find_element(By.CLASS_NAME, 'card-author').text
                date_published = self.driver.find_element(By.CLASS_NAME, 'tags').find_element(By.TAG_NAME, 'time').text
                n["date_published"] = date_published
                n["publisher_name"] = publisher_name
                n["detail_content"] = detail_content
            except (WebDriverException, AttributeError, Exception) as e:
                print(f"An error occurred while scraping content page of category {n.get('category')} and url {n.get('article_url')}:: {e}")
        return news
