from simhash import Simhash, SimhashIndex
import re
from main import readJsonData, preprocessing
from sklearn.model_selection import train_test_split
from pprint import pprint as pp
from nltk.tokenize import word_tokenize


def get_features(s):
    #s = word_tokenize(s)
    # return [s[i] for i in range(max(len(s), 1))]
    width = 5
    s = word_tokenize(s)
    return [' '.join(s[i:i + width]) for i in range(max(len(s) - width + 1, 1))]


def simhash_1(labels, targets, query, query_url):
    dictionary = dict(zip(labels, targets))
    objs = [(str(k), Simhash(get_features(v))) for k, v in dictionary.items()]
    index = SimhashIndex(objs, k=30)
    #print (index.bucket_size())
    # pp(get_features(query))
    query_simhash = Simhash(get_features(query))
    # pp(str(len(index.get_near_dups(query_simhash))))
    print("QUERY: {}".format(query_url))
    pp(index.get_near_dups(query_simhash))


def main():
    # Get data
    data = readJsonData('./dataset/politifact_results.json')

    # Split for Cross Validation
    x_train, x_test = train_test_split(
        data, test_size=0.2, random_state=1234)  # test = 40%, train = 60%

    for i in x_test.index:
        # Set query and targets
        query = ' '.join(preprocessing(data['original_article.content'][i]))
        query_url = data['original_article.url'][i]
        targets = []
        labels = []
        for v in data['extracted_articles'][i]:
            # Content must be more than n_grams length
            if not v or not v['content'] or not v['title'] or not v['url']:
                continue
            # Preprocessing
            preprocessed_content = preprocessing(v['content'])
            string_preprocessed_content = ' '.join(preprocessed_content)
            targets.append(string_preprocessed_content)
            labels.append(v['url'])
        simhash_1(labels, targets, query, query_url)
        print('-'*50)


if __name__ == "__main__":
    main()
