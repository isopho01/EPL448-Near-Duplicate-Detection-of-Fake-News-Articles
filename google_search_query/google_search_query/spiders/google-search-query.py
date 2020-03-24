import scrapy
from urllib.parse import urlencode


class GoogleSearchSpider(scrapy.Spider):
    name = "quotes"
    query = "BREAKING: First NFL Team Declares Bankruptcy Over Kneeling Thugs"
    url = {'q': query, 'num': 100, 'lr': 'lang_en', 'ie': 'utf-8', 'oe': 'utf-8', 'aq': 't'}
    start_urls = ['https://www.google.com/search?' + urlencode(url)]

    def parse(self, response):
        # self.logger.info('hello this is my first spider')
        quotes = response.css('div#search div.g')
        for quote in quotes:
            print('f'*100 + quote)
            yield {
                'url': quote.css('a::attr(href)').get(),
            }

        next_page = response.css('div#foot table tr:first-child td:last-child a::attr(href)').get()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
