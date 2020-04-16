from collections import OrderedDict
from snapy import MinHash, LSH
from simhash import Simhash, SimhashIndex
import re
from main import readJsonData, preprocessing
from pprint import pprint as pp


def get_features(s):
    width = 3
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


def simhash_1(labels, targets, query, query_url):
    dictionary = dict(zip(labels, targets))
    objs = [(str(k), Simhash(get_features(v))) for k, v in dictionary.items()]
    index = SimhashIndex(objs, k=10)
    #print (index.bucket_size())
    #pp(get_features(query))
    query_simhash = Simhash(get_features(query))
    pp(str(len(index.get_near_dups(query_simhash))))

def main():
    # Get data
    data = readJsonData('./dataset/politifact_results.json')
    # Set query and targets
    query = ' '.join(preprocessing(data['original_article.content'][0]))
    query_url = data['original_article.url'][0]
    targets = []
    labels = []
    for v in data['extracted_articles'][0]:
        # Content must be more than n_grams length
        if not v or not v['content'] or not v['title'] or not v['url']:
            continue
        # Preprocessing
        preprocessed_content = preprocessing(v['content'])
        string_preprocessed_content = ' '.join(preprocessed_content)
        targets.append(string_preprocessed_content)
        labels.append(v['url'])
    simhash_1(labels, targets, query, query_url)


if __name__ == "__main__":
    main()
