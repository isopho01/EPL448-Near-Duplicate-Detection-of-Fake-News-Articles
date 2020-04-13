import pprint as pp
import pandas as pd
from google_search import GoogleSearch
from extract_articles import extract_articles
import json
import sys


def createDataset(chosen_dataset):
    if chosen_dataset == 0:
        json_path = './dataset/politifact_results.json'
        dataset = './dataset/politifact_fake.csv'
    elif chosen_dataset == 1:
        json_path = './dataset/gossipcop_results.json'
        dataset = './dataset/gossipcop_fake.csv'
    else:
        sys.exit('Give correct argument')

    # Check json file
    try:
        # Remove closing last two lines from file
        f = open(json_path, "r")
        d = f.read()
        f.close()
        m = d.split("\n")
        s = "\n".join(m[:-2]) + '\n'
        f = open(json_path, "w+")
        for i in range(len(s)):
            f.write(s[i])
        f.close()
    except IOError:
        # Create json file
        with open(json_path, 'w') as f:
            f.write('{\n\t"data": [\n')
    finally:
        f.close()

    with open(json_path, 'a') as f:
        # Read csv and setup Google Client
        df = pd.read_csv(dataset)
        google = GoogleSearch()

        # Do Loop here
        for i in range(433):

            # Pick next query
            current = df.iloc[i]
            original_article = extract_articles(current['news_url'])
            # print('Google search for ' + current['title'])

            # Run query and get results
            res = google.run(current['title'])
            # print('Results of length ' + str(len(res)) + ': ')
            # pp.pprint(res)

            # Extract content for one article
            extracted_articles = [extract_articles(i) for i in res]

            new_entry = dict({'id': i, 'original_article': original_article,
                            'extracted_articles': extracted_articles})
            # pp.pprint(new_entry)

            json.dump(new_entry, f, sort_keys=False, indent=2)
            f.write(',\n')

            # Close json
            f.write('\n]\n}')
            f.close()


if __name__ == '__main__':
    createDataset(0)
