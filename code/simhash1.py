from simhash import Simhash, SimhashIndex
import re
from main import readJsonData, preprocessing, appendToDataset, appendToFingerprints
from sklearn.model_selection import train_test_split
from pprint import pprint as pp
from nltk.tokenize import word_tokenize


def get_features(s, width=5):
    #s = word_tokenize(s)
    # return [s[i] for i in range(max(len(s), 1))]
    s = word_tokenize(s)
    return [' '.join(s[i:i + width]) for i in range(max(len(s) - width + 1, 1))]


def simhash_1(labels, targets, query, query_url, dataset, k=2, width=5):
    dictionary = dict(zip(labels, targets))
    objs = [(str(k), Simhash(get_features(v, width)))
            for k, v in dictionary.items()]
    index = SimhashIndex(objs, k=k)
    query_simhash = Simhash(get_features(query, width))
    near_dups = index.get_near_dups(query_simhash)

    # Save fingerprints for future use
    appendToFingerprints(dataset, './dataset/fingerprints.csv', {"query": str(
        query_simhash.value), "duplicates": ' '.join([str(obj[1].value) for obj in objs])})
    # print("QUERY: {}".format(query_url))
    # pp(near_dups)

    return {"dataset": dataset, "query": query_url, "duplicates": ' '.join(near_dups)}


def main(check):
    # Get data
    data = readJsonData('./dataset/politifact_results.json')
    dataset = []

    # Set settings
    checking = 'politifact'
    k = 15
    random_state = 1234
    width = 3

    # Split for Cross Validation
    # x_train, x_test = train_test_split(
    #     data, test_size=0.2, random_state=random_state)  # test = 40%, train = 60%

    for i in data.index:
        if i % 250 == 0:
            print(str(i))
        # Set query and targets
        query = ' '.join(preprocessing(data['original_article.content'][i]))
        query_url = data['original_article.url'][i]
        targets = []
        labels = []
        for v in data['extracted_articles'][i]:
            # Remove non necessary elements
            if check == 1:
                # Content must be more than n_grams length
                if not v or not v['content'] or not v['title'] or not v['url']:
                    continue

                # Preprocessing
                preprocessed_content = preprocessing(v['content'])
                string_preprocessed_content = ' '.join(preprocessed_content)
                targets.append(string_preprocessed_content)
                labels.append(v['url'])

            # Dont remove them
            else:
                # Content must be more than n_grams length
                if not v or not v['content'] or not v['title'] or not v['url']:
                    targets.append("")
                    labels.append("Empty" + str(i))
                    i += 1
                else:
                    # Preprocessing
                    preprocessed_content = preprocessing(v['content'])
                    string_preprocessed_content = ' '.join(
                        preprocessed_content)
                    targets.append(string_preprocessed_content)
                    labels.append(v['url'])

        dataset.append(simhash_1(labels, targets, query,
                                 query_url, checking, k, width))
        # print('-'*50)

    appendToDataset("./dataset/simhash_dataset.csv", dataset)


if __name__ == "__main__":
    main(1)
