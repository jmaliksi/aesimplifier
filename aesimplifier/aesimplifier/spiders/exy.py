import re
import scrapy
from aesimplifier.items import Post


class Exy(scrapy.Spider):
    name = "exy"
    allowed_domains = ["archipelagoexodus.proboards.com"]
    start_urls = [
        "http://archipelagoexodus.proboards.com/thread/3503/dis-orientation",
        "http://archipelagoexodus.proboards.com/thread/3503/dis-orientation?page=2",
        "http://archipelagoexodus.proboards.com/thread/3503/dis-orientation?page=3",
        "http://archipelagoexodus.proboards.com/thread/3503/dis-orientation?page=4",
        "http://archipelagoexodus.proboards.com/thread/3503/dis-orientation?page=5",
    ]

    def parse(self, response):
        title = response.selector.xpath('//h1').extract()[0]
        posts = response.selector.xpath('//tr[contains(@class, "post")]')
        for post in posts:
            p = Post()
            p['poster'] = post.xpath('td/table/tr/td/div/a[contains(@class, "user-link")]/text()').extract()[0]
            p['content'] = post.xpath('td/table/tr/td/article/div[@class="message"]').extract()[0]
            p['post_id'] = post.xpath('@id').extract()[0]
            p['title'] = title
            yield p

        '''
        # go to next page if it exists
        page_match = re.match(r'(.*)\?page=(\d+)', response.url)
        url = page_match.group(1) if page_match else response.url
        page = int(page_match.group(2)) if page_match else 1
        yield scrapy.Request('{}?page={}'.format(url, page + 1), callback=self.parse)
        '''
