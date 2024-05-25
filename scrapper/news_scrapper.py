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

class AlainNewsCategory(Enum):
    POLITICS = 'politics'
    SOCIAL = 'social'
    ECONOMY = 'economy'
    VARIETIES = 'varities'
    SPORT = 'sports'


class AlainNewsButton(Enum):
    LOADING = "ተጨማሪ ጫን"
    NEXT_PAGE = 'next page'


class AlainNewsScraper:
    def __init__(
            self,
            url: str,
            headless: bool = True,
            number_of_pages_to_scrape: int = 1
    ) -> None:
        """
        Initialize the AlainNewsScraper object

        Args:
            url (str): The URL of the Alain news website
            headless (bool, optional): Whether to run the web driver in headless mode. Defaults to True.
            number_of_pages_to_scrape (int, optional): The number of pages of articles to scrape. Defaults to 1.
        """
        # Create a new instance of the Chrome web driver
        # We use headless mode to avoid seeing the browser window pop up
        # in the background while the script is running
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
        """
        Scrolls the web page to the bottom using JavaScript.

        This function executes a JavaScript command to scroll the web page to the bottom.
        It uses the `execute_script` method of the `driver` object to execute the command.
        The command is `"window.scrollTo(0, document.body.scrollHeight);"`, which scrolls the page
        to the bottom by setting the scroll position to the maximum height of the document body.

        Raises:
            WebDriverException: If an error occurs while scrolling to the bottom of the page.

        Returns:
            None
        """
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except WebDriverException as e:
            print("WebDriverException error occurred while scrolling to the bottom of the page:", e)
            raise

    def initialize_driver(self, category: AlainNewsCategory) -> None:
        """
        Initializes the web driver and navigates to the specified category page.

        Args:
            category (AlainNewsCategory): The category to navigate to.

        Raises:
            WebDriverException: If an error occurs while navigating to the category page.

        Returns:
            None
        """
        category_page_url = f"{self.url}/section/{category.value}/"

        try:
            self.driver.get(category_page_url)
        except WebDriverException as e:
            print("WebDriverException error occurred while navigating to the category page:", e)
            raise

    def get_all_articles_on_page_by_category(self) -> list[WebElement]:
        """
        Retrieves all the articles on the current page for a given category.

        This function performs the following steps:

            1. Scrolls to the bottom of the page to load more articles, if available.
            2. Retrieves the next page element and checks if it is still loading.
            3. If it is, waits until the loading is complete and retrieves the articles element.

        Returns:
            list[WebElement]: A list of WebElement objects representing the articles on the current page for the given category.

        Raises:
            WebDriverException: If an error occurs while retrieving the article elements.
        """

        # Scroll to the bottom of the page to load more articles
        try:
            self.scroll_to_bottom()
        except WebDriverException as e:
            print("WebDriverException error occurred while scrolling to the bottom of the page:", e)
            raise

        # Retrieve the next page element and check if it is still loading
        next_page = self.get_next_page_element()
        while next_page.text == AlainNewsButton.LOADING.value:
            try:
                # If it is, wait until the loading is complete and retrieve the articles element
                next_page = self.get_next_page_element()
            except WebDriverException as e:
                print("WebDriverException error occurred while waiting for the next page element to load:", e)
                raise

        # Return the articles element
        try:
            return self.get_articles_element()
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the article elements:", e)
            raise

    def get_articles_element(self) -> list[WebElement]:
        try:
            row_element = self.driver.find_element(By.XPATH, '//div[@class="row loadmore"]')
            articles = row_element.find_elements(By.TAG_NAME, 'article')
            if not articles:
                print("No articles found on the page.")
            return articles
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the article elements:", e)
            return []

    def get_next_page_element(self) -> WebElement:
        try:
            footer_element = self.driver.find_elements(By.TAG_NAME, 'footer')[0]
            return footer_element.find_element(By.TAG_NAME, 'a')
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the next page element:", e)
            raise

    def get_image_url(self, article: WebElement) -> str:
        try:
            image_element = article.find_element(By.TAG_NAME, 'img')
            image_url = image_element.get_attribute('srcset')
            image_url = re.sub(r'\s\d+w', '', image_url).split(',')[0]
            return image_url.strip()
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the image url of the article:", e)
            return ""

    def get_title(self, article: WebElement) -> str:
        try:
            title_element = article.find_element(By.CLASS_NAME, 'card-title').find_element(By.TAG_NAME, 'a')
            return title_element.text
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the title of the article:", e)
            return ""

    def get_article_url(self, article: WebElement) -> str:
        try:
            title_element = article.find_element(By.CLASS_NAME, 'card-title').find_element(By.TAG_NAME, 'a')
            return title_element.get_attribute('href')
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the article url of the article:", e)
            return ""

    def get_highlight(self, article: WebElement) -> str:
        try:
            highlight_element = article.find_element(By.CLASS_NAME, 'card-text')
            return highlight_element.text
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the highlight of the article:", e)
            return ""

    def get_time_publish(self, article: WebElement) -> str:
        try:
            time_element = article.find_element(By.TAG_NAME, 'time')
            return time_element.text
        except WebDriverException as e:
            print("WebDriverException error occurred while retrieving the time publish of the article:", e)
            return ""

    def get_news(self) -> list[dict]:
        """
        Retrieves news articles from various categories using web scraping.

        This function first initializes the web driver for each category in the AlainNewsCategory enum.
        Then, it navigates to each page of the given category and retrieves all the articles on that page.
        For each article, it retrieves the following information:

            - The image URL of the article
            - The title of the article
            - The URL of the article
            - The highlight/summary of the article
            - The time the article was published
            - The category of the article

        Raises:
            WebDriverException: If there is an error with the web driver.
            AttributeError: If an attribute is not found.
            Exception: If any other error occurs during scraping.
        """
        news = []  # List to store all the news articles
        for category in AlainNewsCategory:  # Iterate through all categories
            self.initialize_driver(category)  # Initialize the web driver for the given category
            pages_to_scrape = self.number_of_pages_to_scrape  # Get the number of pages to scrape for the given category
            while pages_to_scrape > 0:  # While there are still pages to scrape
                pages_to_scrape -= 1  # Decrement the number of pages to scrape
                articles = self.get_all_articles_on_page_by_category()  # Get all the articles on the current page
                if not articles:  # If there are no articles on the current page
                    print(
                        f"No articles found on page {pages_to_scrape + 1} of category {category.value}")  # Print an error message
                else:  # If there are articles on the current page
                    for article in articles:  # Iterate through all the articles on the current page
                        try:
                            news.append(  # Create a dictionary for the current article
                                {
                                    "image_url": self.get_image_url(article),  # The URL of the article's image
                                    "title": self.get_title(article),  # The title of the article
                                    "article_url": self.get_article_url(article),  # The URL of the article
                                    "highlight": self.get_highlight(article),  # The highlight/summary of the article
                                    "time_publish": self.get_time_publish(article),
                                    # The time the article was published
                                    "category": category.value  # The category of the article
                                }
                            )
                        except (WebDriverException, AttributeError, Exception) as e:  # Catch any errors during scraping
                            print(
                                f"An error occurred while scraping article on page {pages_to_scrape + 1} of category {category.value}:",
                                e)  # Print an error message
                next_page = self.get_next_page_element()  # Get the next page element
                if next_page.text == AlainNewsButton.NEXT_PAGE.value and pages_to_scrape > 0:  # If the next page element says "Next Page" and there are still pages to scrape
                    self.driver.execute_script("arguments[0].click();", next_page)  # Click the next page element
                else:  # If the next page element does not say "Next Page" or there are no more pages to scrape
                    break  # Break out of the loop
        return news  # Return the list of news articles

    def get_full_news(self) -> list[dict]:
        """
        Retrieves all the news articles and their corresponding content.

        This function first retrieves all the news articles using the `get_news` method.
        Then, for each article, it navigates to the content page of the article and retrieves
        the following information:

            - The date the article was published
            - The name of the publisher of the article
            - The content of the article

        The retrieved information is then added to the existing information of the article
        as a dictionary and the updated dictionary is returned.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents a news article
                and its corresponding content.
        """
        news = self.get_news()
        for n in news:
            # print("The article on page of category {} is: {}".format(n.get('category'), n.get('article_url')))
            try:
                # Navigate to the content page of the article
                self.driver.get(n.get('article_url'))

                # Retrieve the content of the article
                detail_content = self.driver.find_element(By.ID, 'content-details').text

                # Retrieve the publisher name of the article
                publisher_name = self.driver.find_element(By.CLASS_NAME, 'card-author').text

                # Retrieve the date the article was published
                date_published = self.driver.find_element(By.CLASS_NAME, 'tags').find_element(By.TAG_NAME, 'time').text

                # Add the retrieved information to the existing information of the article
                # as a dictionary
                n["date_published"] = date_published
                n["publisher_name"] = publisher_name
                n["detail_content"] = detail_content

            except (WebDriverException, AttributeError, Exception) as e:
                print(
                    f"An error occurred while scraping content page of category {n.get('category')} and url {n.get('article_url')}:: {e}")
        return news

    # Quit the web driver
    # This method closes the web driver and terminates the underlying browser process
    # It is generally a good practice to quit the web driver as soon as you are
    # finished using it to free up system resources
    def quit_driver(self):
        """
        Quit the web driver

        This method closes the web driver and terminates the underlying browser process
        It is generally a good practice to quit the web driver as soon as you are
        finished using it to free up system resources
        """
        self.driver.quit()