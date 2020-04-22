import re
from main import readJsonData
import pandas as pd
import pprint as pp
from collections import Counter

def count_domains(data):
    domains = Counter(k for k in data)
    for domain, count in domains.most_common():
        print(domain, count)

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


# urls = ["https://web.archive.org/web/20171027105356/http://www.religionmind.com:80/2017/10/saudi-arabia-behead-6-school-girls-for.html",
# "https://web.archive.org/web/20171027105356/www.religionmind.com:80/2017/10/saudi-arabia-behead-6-school-girls-for.html",
# "https://web.archive.org/web/20171027105356/religionmind.com:80/2017/10/saudi-arabia-behead-6-school-girls-for.html",
# "https://web.archive.org/web/20171027105356/http://religionmind.com:80/2017/10/saudi-arabia-behead-6-school-girls-for.html",
# "https://web.archive.org/web/20171027105356/https://www.religionmind.com:80/2017/10/saudi-arabia-behead-6-school-girls-for.html",
# "https://web.archive.org/web/20171027105356/https://religionmind.com:80/2017/10/saudi-arabia-behead-6-school-girls-for.html",
# "http://www.religionmind.com:80/2017/10/saudi-arabia-behead-6-school-girls-for.html",
# "www.religionmind.com:80/2017/10/saudi-arabia-behead-6-school-girls-for.html",
# "religionmind.com:80/2017/10/saudi-arabia-behead-6-school-girls-for.html",
# "http://religionmind.com:80/2017/10/saudi-arabia-behead-6-school-girls-for.html",
# "https://www.religionmind.com:80/2017/10/saudi-arabia-behead-6-school-girls-for.html",
# "https://religionmind.com:80/2017/10/saudi-arabia-behead-6-school-girls-for.html"]
# pp.pprint(parseUrl(urls))
def main():
    dataset = './dataset/simhash_dataset.csv'
    df = pd.read_csv(dataset)
    domains = parseUrl([url for url in [dup for dup in df['duplicates']]])


if __name__ == "__main__":
    main()
