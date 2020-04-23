import re
from main import readJsonData
import pandas as pd
from pprint import pprint as pp
from collections import Counter
import math
import statistics
import json


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
    #Where df was parsed from json-dict using json_normalize
    with open(json_path, 'w') as f:
        json.dump({"data": to_formatted_json(data, sep=".")}, f, sort_keys=False, indent=2)


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
    # # LSH
    # main('./dataset/lsh_dataset.csv', 'politifact')
    # main('./dataset/lsh_dataset.csv', 'gossipcop')
    # main('./dataset/lsh_dataset.csv')
    # # Simhash
    # main('./dataset/simhash_dataset.csv', 'politifact')
    # main('./dataset/simhash_dataset.csv', 'gossipcop')
    # main('./dataset/simhash_dataset.csv')

    getSampleData('./dataset/gossipcop_results.json',
                  './dataset/sample_manual_checking.json')
