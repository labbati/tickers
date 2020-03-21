
import logging
import scrapy
import json


class NyseSpider(scrapy.Spider):
    name = 'NYSE'
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'
    url_template = 'https://www.nasdaq.com/api/v1/screener?page={}&pageSize=100'
    start_urls = [
        url_template.format(1)
    ]

    def __init__(self, name=None, **kwargs):
        scrapy.Spider.__init__(self, name=name, **kwargs)
        self.page = 1

    def start_requests(self):
        yield self.build_request(1)

    def build_request(self, page):
        body = json.dumps({
            'instrumentType': 'EQUITY',
            'pageNumber': page,
            'sortColumn': 'NORMALIZED_TICKER',
            "maxResultsPerPage": 10, "filterToken": ""})
        self.logger.info(body)
        return scrapy.Request(
            url='https://www.nyse.com/api/quotes/filter',
            method='POST',
            headers={'content-type': 'application/json'},
            body=body
        )

    def parse(self, response):
        self.logger.info(response.body_as_unicode())
        data = json.loads(response.body_as_unicode())
        for stock in data:
            yield {
                'market': self.name,
                'ticker': stock['normalizedTicker'],
                'company': stock['instrumentName'],
            }

        if len(data) > 0:
            self.page = self.page + 1 if self.page else 2
            yield self.build_request(self.page)
