import scrapy


class HNSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://news.ycombinator.com/',
    ]

    def parse(self, response):
        for post in response.css('tr.athing td:nth-of-type(3)'):
            # self.logger.debug("Post >>>>>>>>>>>>>>>>> %s", post)
            self.logger.debug("Title %s", post.css('a::text').get())
            self.logger.debug("Url %s", post.css('a::attr("href")').get())
            yield {
                'title': post.css('a::text').get(),
                'url': post.css('a::attr("href")').get(),
            }

        # next_page = response.css('li.next a::attr("href")').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
