
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

class BBCScraper:
  def __init__(self, base_url, prefix):
      self.base_url = base_url
      self.prefix = prefix
      self.soup = self.get_soup(base_url)

  def get_soup(self, url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

  def get_article_urls(self):
      # Find all 'a' elements
      a_elements = self.soup.find_all('a')

      # Extract the href attribute from each 'a' element
      urls = [a['href'] for a in a_elements if a.has_attr('href')]

      # Filter out URLs that don't start with the specified prefix
      filtered_urls = [url for url in urls if url.startswith(self.prefix)]

      return filtered_urls
  
  def get_title(self, soup):
    # Replace with the actual method to extract the title
    title_element = soup.select_one('title')
    return title_element.text if title_element else None

  def get_date(self, soup):
    # Replace with the actual method to extract the date
    date_element = soup.select_one('date')
    return date_element.text if date_element else None

  def get_image_url(self, soup):
    img_element = soup.select_one('img')
    return img_element['src'] if img_element else None

  def get_content(self, soup):
    p_elements = soup.select('p')
    return ' '.join(p.text for p in p_elements)

  def get_source(self, url):
    parsed_url = urlparse(url)
    return parsed_url.netloc
  
  def get_word_count(self, soup):
      content = self.get_content(soup)
      return len(content.split())

  def get_tags(self, soup):
        # Replace with the actual method to extract the tags
        tag_elements = soup.select('tag')
        return [tag.text for tag in tag_elements]

  def get_category(self, soup):
    # Replace with the actual method to extract the category
    category_element = soup.select_one('category')
    return category_element.text if category_element else None


  def to_dict(self, url):
      soup = self.get_soup(url)
      return {
          'url': url,
          'title': self.get_title(soup),
          'date': self.get_date(soup),
          'image_url': self.get_image_url(soup),
          'text': self.get_content(soup),
          'source': self.get_source(url),
          'word_count': self.get_word_count(soup),
          'tags': self.get_tags(soup),
          'language': 'am',
          'category': self.get_category(soup),
      }

  def get_articles(self):
    article_urls = self.get_article_urls()
    return [self.to_dict(url) for url in article_urls]