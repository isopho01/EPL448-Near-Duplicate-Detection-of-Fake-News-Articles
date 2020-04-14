from pprint import pprint as pp
import pandas as pd
import json
from pandas import json_normalize
import sys


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


def main():
    data = readJsonData('./dataset/politifact_results.json')
    if data.empty:
        sys.exit('File not found')
    print(data)


if __name__ == '__main__':
    main()
