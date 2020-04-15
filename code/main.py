from pprint import pprint as pp
import pandas as pd
from pandas import json_normalize
import sys
import nltk
import json
import re
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def readJsonData(filePath):
    # data: id    extracted_articles[0-202][0-30(max)]    original_article.title  original_article.content  original_article.url
    #                       title, content, url
    try:
        with open(filePath) as f:
            data = json.load(f)
        data = json_normalize(data['data'])
    except:
        return pd.DataFrame()

    return data


def preprocessing(sentence):
    # Clean up noise
    sentence = sentence.strip().lower()
    sentence = re.sub(r'[^\w]+', ' ', sentence)

    # Tokenize sentence
    words = word_tokenize(sentence)

    # Create models
    # ps = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # For each word
    content = []
    for i in range(len(words)):
        if not words[i] in stop_words:  # Stop Words
            word = words[i]
            # word = ps.stem(word)    # Stemming
            word = lemmatizer.lemmatize(word)   # Lemmatize
            content.append(word)

    return ' '.join(content)


def main():
    # data = readJsonData('./dataset/politifact_results.json')
    # if data.empty:
    #     sys.exit('File not found')
    # print(data)
    sentence = "Western countries are being urged to intervene in a case where 6 young school girls facing execution for acting indecently at a friends house.\n\nFathima Al Kwaini and her friends that included three male friends have celebrated\n\nKwaini's\n\nbirthday at a friends house. A neighbor supposedly an assistant of an Imam of a mosque close by has reported this to Saudi Arabia's religious police. When the police arrived the girls were dancing with their male friends and they were arrested immediately.\n\n\n\n\n\n\n\n\n\nThe ultra conservative Arabian nation that has one of the worst human rights records is also a member of the United Nations Human Rights commission and recently got elected to the Women's Rights Commission as well which sparked anger and protest.\n\nAccording to HRW the girls were detained for more than a year before the trial and never confessed committing any crime. However the verdict of the \"male only\" Sharia panel was that they need o be executed in accordance with the Sharia law. The boys were only advised \"not to be victimized\" the report further states.\n\n\n\n\n\nSaudi uses methods such as beheading, stoning and crucifixion to execute women for crimes, including adultery, in the strict Islamic country. Beheadings take place in public squares where the headless corpses are later put on display."
    print(preprocessing(sentence))

if __name__ == '__main__':
    main()
