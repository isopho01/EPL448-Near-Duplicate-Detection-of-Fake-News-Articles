import requests
from bs4 import BeautifulSoup
import pprint


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
    queries = ["BREAKING: First NFL Team Declares Bankruptcy Over Kneeling Thugs",
               "Court Orders Obama To Pay $400 Million In Restitution",
               "UPDATE: Second Roy Moore Accuser Works For Michelle Obama Right NOW -",
               "Oscar Pistorius Attempts To Commit Suicide",
               "Trump Votes For Death Penalty For Being Gay",
               "Putin says: ‘Pope Francis Is Not A Man Of God’ | Must-See !!",
               "New York Man Wanted For Infecting 240 Men And Women With HIV!!!",
               "Saudi Arabia to Behead 6 School Girls for Being With Their Male Friends Without Parents or a Guardian",
               "Malia Obama Fired From Cushy Internship At Spanish Embassy",
               "Target to Discontinue Sale of Holy Bible"]

    google = GoogleSearch()
    [pprint.pprint(google.run(j)) for j in queries]


if __name__ == '__main__':
    main()
