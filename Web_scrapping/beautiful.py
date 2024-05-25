#from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import re


url ="https://am.wikipedia.org/wiki/%E1%8B%A8%E1%8A%A2%E1%89%B5%E1%8B%AE%E1%8C%B5%E1%8B%AB_%E1%8A%90%E1%8C%88%E1%88%A5%E1%89%B3%E1%89%B5"


html = urlopen(url)


# Fetch the HTML content
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

# Extract text from paragraphs (adjust selector as needed)

texts = soup.find_all("p")
list_texts = []

for text in texts:
    lines = text.get_text(strip=True)
    str_lines = str(lines)
    clean = re.compile('<.*==?>') #compiles a regular expression pattern
    clean2 = (re.sub(clean, '' ,str_lines)) # used the re.sub() method to replace any matches of this pattern in str_cells with an empty string
    list_texts.append(clean2)

print(list_texts)

#text_df = pd.DataFrame(list_texts)
#df1 = text_df[0].str.split('·', expand=True)
#df1[0] = df1[0].str.strip('[')
#df1#

