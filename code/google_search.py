import requests
from bs4 import BeautifulSoup
import pprint
from extract_articles import extract_articles


class GoogleSearch:
    def __init__(self):
        self.USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        self.MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, " \
                                 "like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36 "

    def run(self, query):
        query = query.replace(' ', '+')
        url = f"https://google.com/search?q={query}&lr=lang_en&num=100&start=0"

        headers = {"user-agent": self.USER_AGENT}
        resp = requests.get(url, headers=headers)
        results = []

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            for g in soup.find_all('div', class_='r'):
                anchors = g.find_all('a')
                if anchors:
                    results.append(anchors[0]['href'])

            return results
        else:
            print(f"HTTP Error {resp.status_code}")

        return None


def main():
    google = GoogleSearch()
    res = google.run('UPDATE: Second Roy Moore Accuser Works For Michelle Obama Right NOW -')[0]
    pprint.pprint(extract_articles(res))


if __name__ == '__main__':
    main()
