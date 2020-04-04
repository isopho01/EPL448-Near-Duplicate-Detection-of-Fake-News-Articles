import pandas as pd
import time
import logging
import json
import requests
import csv 
from collections import OrderedDict
#from pandas import csv
from newspaper import Article 




def get_web_archieve_results(search_url):
    try:
        archieve_url = "http://web.archive.org/cdx/search/cdx?url={}&output=json".format(search_url)

        response = requests.get(archieve_url)
        response_json = json.loads(response.content)

        response_json = response_json[1:]

        return response_json

    except:
        return None
    
def get_website_url_from_arhieve(url):
    """ Get the url from http://web.archive.org/ for the passed url if exists."""
    archieve_results = get_web_archieve_results(url)
    if archieve_results:
        modified_url = "https://web.archive.org/web/{}/{}".format(archieve_results[0][1], archieve_results[0][2])
        return modified_url
    else:
        return None
    
    
def extract_articles(url):
    try:
        if 'http' not in url:
            if url[0] == '/':
                url = url[1:]
            try:
                article = Article('http://' + url)
                article.download()
                time.sleep(2)
                article.parse()
                flag = True
            except:
                logging.exception("Exception in getting data from url {}".format(url))
                flag = False
                pass
            if flag == False:
                try:
                    article = Article('https://' + url)
                    article.download()
                    time.sleep(2)
                    article.parse()
                    flag = True
                except:
                    logging.exception("Exception in getting data from url {}".format(url))
                    flag = False
                    pass
            if flag == False:
                return None
        else:
            try:
                article = Article(url)
                article.download()
                time.sleep(2)
                article.parse()
            except:
                logging.exception("Exception in getting data from url {}".format(url))
                return None

        if not article.is_parsed:
            return None
        json = ''
        title = article.title
        content = article.text
        json = { 'url': url,'title': title,'content': content }
        print(json)
        
        
    except:
        logging.exception("Exception in fetching article form URL : {}".format(url))
    return json
        
        
        
def read_articles():
    # now we will open a file for writing 
    data_file = open('data_file.csv', 'w', encoding='utf-8-sig') 
      
    # # create the csv writer object 
    # csv_writer = csv.writer(data_file)
    # header = { 'url', 'title', 'content'}
    # ordered_fieldnames = OrderedDict([('url',None),('title',None),('content',None)])
    # dw = csv.DictWriter(data_file, delimiter=',', fieldnames=ordered_fieldnames)
    # dw.writeheader()
    #csv_writer.writerow(header)
    
    #read csv
    news_artcle=''
    row = ''
    i = 0
    col_list = ["news_url"]
    df = pd.read_csv("gossipcop_fake.csv", usecols=col_list,encoding='utf-8-sig')
    for url in df["news_url"]:
         news_artcle=''
         news_article = extract_articles(url)
         if news_article is None:
            archieve_url = get_website_url_from_arhieve(url)
            if archieve_url is not None:
                news_article = extract_articles(archieve_url)
         if(news_article != None):
            print(news_article)
            y = json.dumps(news_article)
             
            #dw.writerow(news_article)
       
    data_file.close()     
         
        
     
read_articles()       
        

