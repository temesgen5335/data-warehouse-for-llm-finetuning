import re

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.mongodb import MongoDB
from data_cleaning_utils import Normalize

archive_db = MongoDB('archive', 'archive_data', 'mongodb://mongodb:27017/')

def process_and_display(text):
    # create an instance of the Normalize class
    normalizer = Normalize()

    # Test the function
    print("\nOriginal text: ")
    print(text)

    preprocessed_text = normalizer.clean_data(text)
    print("\n Preprocessed text:")
    print(preprocessed_text, "\n")

    print("==================Success==========================")


    return preprocessed_text


def save_to_db():
    pass









def main():
    text = "ጽኑ ህክምና የሚያስፈልጋቸው ሲሆኑ፤ ከዚህ ውስጥ ከ40 እስከ"
    clean_text = process_and_display(text)

if __name__ == '__main__':
    main()