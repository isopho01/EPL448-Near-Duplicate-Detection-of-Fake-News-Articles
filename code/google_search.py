import os
import sys

import requests
from bs4 import BeautifulSoup
import json
import time
import random
from csv import writer
from csv import DictWriter


class GoogleSearch:
    def __init__(self, filename="data.csv"):
        self.USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        self.MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, " \
                                 "like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36 "
        self.numOfQueries = 0
        self.timeout = 0
        self.filename = filename

    def append_list_as_row(self, list_of_elem):

        # Write header
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write('query,results\n')

        # Open file in append mode
        with open(self.filename, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = writer(write_obj)
            # Add dictionary as wor in the csv
            csv_writer.writerow(list_of_elem)

    def run(self, query):
        encoded_query = query.replace(' ', '+')
        url = f"https://google.com/search?q={encoded_query}&lr=lang_en&num=100&start=0"

        headers = {"user-agent": self.USER_AGENT}
        resp = requests.get(url, headers=headers)
        results = []

        if self.timeout < 5:
            time.sleep(random.randrange(2, 7))  # Random delay in seconds
        else:
            sys.exit(f"Timeout at query {self.numOfQueries}")

        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            for g in soup.find_all('div', class_='r'):
                anchors = g.find_all('a')
                if anchors:
                    results.append(anchors[0]['href'])

            # Add to csv
            self.append_list_as_row([query, results])

            print(self.numOfQueries)
            self.numOfQueries = self.numOfQueries + 1
            self.timeout = 0
        else:
            print(f"HTTP Error {resp.status_code}")
            self.timeout = self.timeout + 1


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
    [google.run(j) for j in queries]
    # dictionary = [{j: google.run(j)} for j in queries]

    # with open('data2.json', 'w') as outfile:
    #     json.dump(dictionary, outfile, sort_keys=True, indent=4)


if __name__ == '__main__':
    main()
