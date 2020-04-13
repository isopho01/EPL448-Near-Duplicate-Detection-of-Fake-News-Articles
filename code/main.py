import pprint as pp
import pandas as pd
from google_search import GoogleSearch
from extract_articles import extract_articles

def main():
    # Read csv and setup Google Client
    df = pd.read_csv('./dataset/politifact_fake.csv')
    google = GoogleSearch()

    # Pick next query
    current = df.iloc[0]
    print('Google search for ' + current['title'])
    print('\n\n')

    # Run query and get results
    res = google.run(current['title'])
    print('Results of length ' + str(len(res)) + ': ')
    pp.pprint(res)
    print('\n\n')

    # Extract content for one article
    extracted_articles = [extract_articles(i) for i in res]
    pp.pprint(str(len(extracted_articles)))



if __name__ == '__main__':
    main()
