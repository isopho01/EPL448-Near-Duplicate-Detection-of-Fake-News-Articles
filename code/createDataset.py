import json
import sys
import re
import pprint as pp
import pandas as pd
from google_search import GoogleSearch
from extract_articles import extract_articles
from extract_articles import get_website_url_from_arhieve


def createDataset(chosen_dataset, n, random_state, skip=0):
    # Set scope variables
    regex = re.compile(
        r'^((http(s?):\/\/)?)((www\.)?)((?!(facebook|twitter|instagram|google|youtube|tumblur|itunes|linkedin|pinterest)).)*\..*$')
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
        df = df.sample(n=n, random_state=random_state)
        index_array = df.index
        google = GoogleSearch()

        # Do Loop here
        for i in range(n):
            if(i < skip):
                continue

            print('\033[92m' + 'Currently checking id #',
                  str(i + 1), 'of', str(n) + '\033[0m')

            # Pick next query
            current = df.iloc[i]

            # Check url if acceptable
            final_url = current['news_url']
            url_check = current['news_url']
            if(current['news_url'] != current['news_url']):
                continue
            if not url_check or not regex.match(url_check):
                continue
            if 'web.archive.org/web/' in url_check:
                # Remove http(s?)web.archive.org/web/[0-9]{14}
                url_check = url_check.split('web.archive.org/web/')[1:]
                url_check = ''.join(url_check)[15:]
            if 'www.' in url_check:
                # Remove www.
                url_check = url_check[(url_check.find('www.') + 4):]
            url_check = ''.join(url_check)
            if not url_check or not regex.match(url_check):
                continue

            # Extract articles from google
            original_article = extract_articles(current['news_url'])
            if original_article is None:
                archieve_url = get_website_url_from_arhieve(
                    current['news_url'])
                if archieve_url is not None:
                    final_url = archieve_url
                    original_article = extract_articles(archieve_url)
                else:
                    continue

            # Check if content is empty
            if not original_article or not original_article['content']:
                continue

            # Run query and get results
            res = google.run(current['title'])

            # Extract content for one article
            extracted_articles = [extract_articles(i) for i in res]

            # Build json entry and save to file
            new_entry = dict({'id': str(index_array[i]), 'original_article': {
                             "url": final_url, "title": current['title'], "content": original_article['content']}, 'extracted_articles': extracted_articles})
            json.dump(new_entry, f, sort_keys=False, indent=2)
            f.write(',\n')

        # Close json
        f.write('\n]\n}')
        f.close()


if __name__ == '__main__':
    n = 432
    random_state = 1234

    # createDataset(0, n, random_state, 0)
    with open('./dataset/politifact_results.json') as f:
        data = json.load(f)
        [print(i['original_article']['url']) for i in data['data']]

