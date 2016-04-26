import re
import scrapy
from aesimplifier.items import Post


class Exy(scrapy.Spider):
    name = "exy"
    allowed_domains = ["archipelagoexodus.proboards.com"]
    start_urls = [
        "http://archipelagoexodus.proboards.com/thread/3503/dis-orientation?page=1",
        # "http://archipelagoexodus.proboards.com/thread/3503/dis-orientation?page=2",
        # "http://archipelagoexodus.proboards.com/thread/3503/dis-orientation?page=3",
        # "http://archipelagoexodus.proboards.com/thread/3503/dis-orientation?page=4",
        # "http://archipelagoexodus.proboards.com/thread/3503/dis-orientation?page=5",
    ]

    def parse(self, response):
        links = response.selector.xpath('//a[re:test(@href, "/thread/\\d*/.*\\?page=\\d+")]/@href').extract()
        for link in links:
            # remove this when we go to full crawling
            if link[:link.index('?')] not in response.url:
                continue
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        title = response.selector.xpath('//h1').extract()[0]
        posts = response.selector.xpath('//tr[contains(@class, "post")]')
        for post in posts:
            p = Post()
            p['poster'] = post.xpath('td/table/tr/td/div/a[contains(@class, "user-link")]/text()').extract()[0]
            p['content'] = post.xpath('td/table/tr/td/article/div[@class="message"]').extract()[0]
            p['post_id'] = post.xpath('@id').extract()[0]
            p['title'] = title
            yield p
