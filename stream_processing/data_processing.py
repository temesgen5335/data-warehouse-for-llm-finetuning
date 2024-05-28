import requests
from bs4 import BeautifulSoup
import re


def clean_data(text):
       
    # Remove ASCII characters and numbers
    cleaned_text = remove_ascii_and_numbers(cleaned_text)
    
    # Remove punctuation and special characters
    cleaned_text = remove_punc_and_special_chars(cleaned_text)
    
    # Normalize character level mismatch
    cleaned_text = normalize_char_level_missmatch(cleaned_text)
    
    return cleaned_text

def remove_ascii_and_numbers(text_input):
    rm_num_and_ascii = re.sub('[A-Za-z0-9]', '', text_input)
    return re.sub('[\'\u1369-\u137C\']+', '', rm_num_and_ascii)

def remove_punc_and_special_chars(text): 
    normalized_text = re.sub('[\!\@\#\$\%\^\«\»\&\*\(\)\…\[\]\{\}\;\“\”\›\’\‘\"\'\:\,\.\‹\/\<\>\?\\\\|\`\´\~\-\=\+\፡\።\፤\;\፦\፥\፧\፨\፣]', '',text)
    return normalized_text

def normalize_char_level_missmatch(input_token):
    rep1 = re.sub('ሃ|ኅ|ኃ|ሐ|ሓ|ኻ', 'ሀ', input_token)
    rep2 = re.sub('ሑ|ኁ|ዅ', 'ሁ', rep1)
    rep3 = re.sub('ኂ|ሒ|ኺ', 'ሂ', rep2)
    rep4 = re.sub('ኌ|ሔ|ዄ', 'ሄ', rep3)
    rep5 = re.sub('ሕ|ኅ', 'ህ', rep4)
    rep6 = re.sub('ኆ|ሖ|ኾ', 'ሆ', rep5)
    rep7 = re.sub('ሠ', 'ሰ', rep6)
    rep8 = re.sub('ሡ', 'ሱ', rep7)
    rep9 = re.sub('ሢ', 'ሲ', rep8)
    rep10 = re.sub('ሣ', 'ሳ', rep9)
    rep11 = re.sub('ሤ', 'ሴ', rep10)
    rep12 = re.sub('ሥ', 'ስ', rep11)
    rep13 = re.sub('ሦ', 'ሶ', rep12)
    rep14 = re.sub('ዓ|ኣ|ዐ', 'አ', rep13)
    rep15 = re.sub('ዑ', 'ኡ', rep14)
    rep16 = re.sub('ዒ', 'ኢ', rep15)
    rep17 = re.sub('ዔ', 'ኤ', rep16)
    rep18 = re.sub('ዕ', 'እ', rep17)
    rep19 = re.sub('ዖ', 'ኦ', rep18)
    rep20 = re.sub('ጸ', 'ፀ', rep19)
    rep21 = re.sub('ጹ', 'ፁ', rep20)
    rep22 = re.sub('ጺ', 'ፂ', rep21)
    rep23 = re.sub('ጻ', 'ፃ', rep22)
    rep24 = re.sub('ጼ', 'ፄ', rep23)
    rep25 = re.sub('ጽ', 'ፅ', rep24)
    rep26 = re.sub('ጾ', 'ፆ', rep25)
    rep27 = re.sub('(ሉ[ዋአ])', 'ሏ', rep26)
    rep28 = re.sub('(ሙ[ዋአ])', 'ሟ', rep27)
    rep29 = re.sub('(ቱ[ዋአ])', 'ቷ', rep28)
    rep30 = re.sub('(ሩ[ዋአ])', 'ሯ', rep29)
    rep31 = re.sub('(ሱ[ዋአ])', 'ሷ', rep30)
    rep32 = re.sub('(ሹ[ዋአ])', 'ሿ', rep31)
    rep33 = re.sub('(ቁ[ዋአ])', 'ቋ', rep32)
    rep34 = re.sub('(ቡ[ዋአ])', 'ቧ', rep33)
    rep35 = re.sub('(ቹ[ዋአ])', 'ቿ', rep34)
    rep36 = re.sub('(ሁ[ዋአ])', 'ኋ', rep35)
    rep37 = re.sub('(ኑ[ዋአ])', 'ኗ', rep36)
    rep38 = re.sub('(ኙ[ዋአ])', 'ኟ', rep37)
    rep39 = re.sub('(ኩ[ዋአ])', 'ኳ', rep38)
    rep40 = re.sub('(ዙ[ዋአ])', 'ዟ', rep39)
    rep41 = re.sub('(ጉ[ዋአ])', 'ጓ', rep40)
    rep42 = re.sub('(ደ[ዋአ])', 'ዷ', rep41)
    rep43 = re.sub('(ጡ[ዋአ])', 'ጧ', rep42)
    rep44 = re.sub('(ጩ[ዋአ])', 'ጯ', rep43)
    rep45 = re.sub('(ጹ[ዋአ])', 'ጿ', rep44)
    rep46 = re.sub('(ፉ[ዋአ])', 'ፏ', rep45)
    rep47 = re.sub('ቊ', 'ቁ', rep46)  # ቁ can be written as ቊ
    rep48 = re.sub('ኵ', 'ኩ', rep47)  # ኩ can be also written as ኵ

    return rep48


