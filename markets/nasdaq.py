
import logging
import scrapy
import json


class NasdaqSpider(scrapy.Spider):
    name = 'nasdaq'
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'
    url_template = 'https://www.nasdaq.com/api/v1/screener?page={}&pageSize=100'
    start_urls = [
        url_template.format(1)
    ]

    def __init__(self, name=None, **kwargs):
        scrapy.Spider.__init__(self, name=name, **kwargs)
        self.page = 1

    def parse(self, response):
        data = json.loads(response.body_as_unicode())['data']
        for stock in data:
            yield {
                'market': self.name,
                'ticker': stock['ticker'],
                'company': stock['company'],
            }

        if len(data) > 0:
            self.page = self.page + 1 if self.page else 2
            next_url = self.url_template.format(self.page)
            yield response.follow(next_url, self.parse)
