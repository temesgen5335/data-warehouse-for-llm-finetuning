from data_cleaning.data_cleaning_utils import Normalize
import re

def main():
    # create an instance of the Normalize class
    normalizer = Normalize()

    # Test the function
    text = input("Enter text: ")

    preprocessed_text = normalizer.clean_data(text)
    print("\n \n Preprocessed text:")
    print(preprocessed_text)

if __name__ == '__main__':
    main()