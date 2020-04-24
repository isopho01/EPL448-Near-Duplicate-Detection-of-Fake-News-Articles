import re
from main import readJsonData
from simhash import Simhash, SimhashIndex
import pandas as pd
from pprint import pprint as pp
import os
from collections import Counter
import math
import statistics
import json
from sklearn.metrics import precision_score, recall_score
import matplotlib.pyplot as plt


def count_domains(data):
    domains = Counter(k for k in data)
    res = []
    for domain, count in domains.most_common():
        res.append({'domain': domain, 'count': count})
    return res


def parseUrl(urls):
    hostnames = []
    for url in urls:
        if not url or url != url:
            continue
        spltAr = url.split("://")
        i = (0, 1)[len(spltAr) > 1]
        dm = spltAr[i].split("?")[0].split('/')[0].split(':')[0].lower()
        if dm.split(".")[0] == 'www':
            dm = '.'.join(dm.split(".")[1:])
        if(dm == 'web.archive.org'):
            dm = re.sub(
                r'^(http(s?)://?)web.archive.org/web/[0-9]{14}/', '', url)
            spltAr = dm.split("://")
            i = (0, 1)[len(spltAr) > 1]
            dm = spltAr[i].split("?")[0].split('/')[0].split(':')[0].lower()
            if dm.split(".")[0] == 'www':
                dm = '.'.join(dm.split(".")[1:])

        hostnames.append(dm)
    return count_domains(hostnames)


def avgDuplicationRate(df):
    return [len(data.split()) for data in df['duplicates'] if data == data]


def checkKnownDomains(domains):
    known = pd.read_csv('./dataset/fake_news_domain_list.csv')
    return [domain for domain in domains if known['domain'].str.contains(domain).any()]


def checkNotKnownDomains(domains):
    known = pd.read_csv('./dataset/fake_news_domain_list.csv')
    return [domain for domain in domains if not known['domain'].str.contains(domain).any()]


def getSampleData(dataset, json_path):
    data = readJsonData(dataset)
    data = data[:100]
    # Where df was parsed from json-dict using json_normalize
    with open(json_path, 'w') as f:
        json.dump({"data": to_formatted_json(data, sep=".")},
                  f, sort_keys=False, indent=2)


def set_for_keys(my_dict, key_arr, val):
    """
    Set val at path in my_dict defined by the string (or serializable object) array key_arr
    """
    current = my_dict
    for i in range(len(key_arr)):
        key = key_arr[i]
        if key not in current:
            if i == len(key_arr)-1:
                current[key] = val
            else:
                current[key] = {}
        else:
            if type(current[key]) is not dict:
                print("Given dictionary is not compatible with key structure requested")
                raise ValueError("Dictionary key already occupied")

        current = current[key]

    return my_dict


def to_formatted_json(df, sep="."):
    result = []
    for _, row in df.iterrows():
        parsed_row = {}
        for idx, val in row.iteritems():
            keys = idx.split(sep)
            parsed_row = set_for_keys(parsed_row, keys, val)

        result.append(parsed_row)
    return result


def get_near_dups(query_simhash, candidates_simhash, k):
    res = [0] * len(candidates_simhash)
    query = Simhash(value=query_simhash)

    for i in range(len(candidates_simhash)):
        candidates_simhash[i] = (str(i), Simhash(value=candidates_simhash[i]))
        i = i + 1
    index = SimhashIndex(candidates_simhash, k=k)
    near_dups = index.get_near_dups(query)

    for dup in near_dups:
        res[int(dup)] = 1

    return res


def createPrecisionRecallCurve(precision, recall, labels):
    precision2 = precision.copy()
    i = len(recall) - 2

    # interpolation...
    while i >= 0:
        if precision[i+1] > precision[i]:
            precision[i] = precision[i+1]
        i = i-1

    # plotting...
    fig, ax = plt.subplots()
    for i in range(len(recall) - 1):
        ax.plot((recall[i], recall[i]), (precision[i],
                                         precision[i+1]), 'k-', label='', color='red')  # vertical
        ax.plot((recall[i], recall[i+1]), (precision[i+1],
                                           precision[i+1]), 'k-', label='', color='red')  # horizontal

    ax.plot(recall, precision2, 'k--', color='blue')
    # plt.legend()
    plt.title('Percision Recall Curve')
    ax.set_xlabel("recall")
    ax.set_ylabel("precision")
    savePlot(plt, "p-r-curve.jpg")
    plt.show()

    plt.close('all')


def createPrecisionRecallPlot(precision, recall, labels):
    plt.plot(labels, precision, 'xk-', label='precision',
             color='black')
    plt.plot(labels, recall, '|k--', label='recall')

    plt.xlabel("Hamming Distance 'k'")
    plt.ylabel("Precision and Recall")
    plt.title("Percision-Recall Graph Varying 'k' for 64-bit SimHash")
    plt.legend()
    savePlot(plt, "precision-recall.jpg")
    plt.show()

    plt.close('all')


def savePlot(plot, file_name):
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'plots/')

    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    plt.savefig(results_dir + file_name)


def main(dataset, dt='None'):
    print('Algorithm:', dt, 'Dataset:', dataset)

    # Read dataset and remove None
    df = pd.read_csv(dataset)
    if dt != 'None':
        df = df.loc[df['dataset'] == dt]

    # Domains
    domains = parseUrl([url for url in [dup for dup in df['duplicates']]])

    # Count known fake domains
    known = len(checkKnownDomains([domain['domain'] for domain in domains]))
    unknown = len(checkNotKnownDomains(
        [domain['domain'] for domain in domains]))
    print('Known Ratio', known / (known + unknown))

    # Duplication Rate
    dup_rate = avgDuplicationRate(df)
    print('Mean:', statistics.mean(dup_rate))
    print('Median:', statistics.median(dup_rate))
    print('Max:', max(dup_rate))

    print('='*30)


if __name__ == "__main__":
    """ Statistical Analysis """
    # LSH
    main('./dataset/lsh_dataset.csv', 'politifact')
    main('./dataset/lsh_dataset.csv', 'gossipcop')
    main('./dataset/lsh_dataset.csv')
    # Simhash
    main('./dataset/simhash_dataset.csv', 'politifact')
    main('./dataset/simhash_dataset.csv', 'gossipcop')
    main('./dataset/simhash_dataset.csv')

    """ Collect a sample of the data """
    # getSampleData('./dataset/gossipcop_results.json',
    #               './dataset/sample_manual_checking.json')

    """ Check k """
    # precision = []
    # recall = []
    # labels = []
    # for k in range(1, 33):
    #     labels.append(k)
    #     y_true = []
    #     y_pred = []

    #     data = readJsonData('./dataset/sample_manual_checking.json')
    #     fingerprints = pd.read_csv('./dataset/fingerprints.csv')
    #     for index, row in data.iterrows():
    #         # Get "true" results
    #         for article in row['extracted_articles']:
    #             if article['dup'] == 2:
    #                 y_true.append(0)
    #             else:
    #                 y_true.append(article['dup'])
    #         fing = fingerprints.iloc[index]
    #         # Get predictions
    #         y_pred.extend(get_near_dups(int(fing['query']), list(
    #             map(int, fing['duplicates'].split(' '))), k))

    #         # TODO remove when done testing
    #         if index == 49:
    #             break

    #     precision.append(precision_score(y_true, y_pred, average='binary'))
    #     recall.append(recall_score(y_true, y_pred, average='binary'))

    # createPrecisionRecallCurve(precision, recall, labels)
    # createPrecisionRecallPlot(precision, recall, labels)
