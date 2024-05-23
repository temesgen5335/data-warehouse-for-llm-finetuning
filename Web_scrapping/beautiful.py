from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Set up Selenium webdriver
driver = webdriver.Firefox()
url = "https://www.ethiobookreview.com/book/ye-ethiopia-tarik-ke-lusi-arat-million"
driver.get(url)
time.sleep(3)  # Let the page load

# Use BeautifulSoup to parse the page source
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find the element containing the text data
text_data_element = soup.find('div', class_='et_pb_module et_pb_text et_pb_text_1 et_pb_bg_layout_light')

if text_data_element:
    # Extract text data
    text_data = text_data_element.get_text()
    print(text_data)
else:
    print("Text data element not found")

# Close the Selenium webdriver
driver.quit()
