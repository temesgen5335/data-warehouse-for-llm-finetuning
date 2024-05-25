import requests
from bs4 import BeautifulSoup
import re


def clean_data(text):
    # Define symbols to remove
    symbols_to_remove = r"[\[\]{}\/\-=+\$]"

    # Remove symbols from the text
    cleaned_text = re.sub(symbols_to_remove, "", text)
    
    return cleaned_text