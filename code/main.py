from urllib.parse import urlencode

query = "BREAKING: First NFL Team Declares Bankruptcy Over Kneeling Thugs"
url = {'q': query, 'num': 100, 'lr': 'lang_en'}
start_urls = ['https://www.google.com/search?' + urlencode(url)]

print(start_urls)