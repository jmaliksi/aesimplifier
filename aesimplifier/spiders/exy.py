import re
import scrapy
from aesimplifier.items import Post


class Exy(scrapy.Spider):
    name = 'exy'
    allowed_domains = ['archipelagoexodus.proboards.com']
    start_urls = [
        'http://archipelagoexodus.proboards.com/board/21/online-role-play',
        'http://archipelagoexodus.proboards.com/board/15/exodus-writing-archive',
    ]
 
    default_topics = [
        '(Dis)Orientation',
        'Chords in an Ethereal Harp',
        'Triannual',
        'Obscured Truth; Court is in Session',
        'Luxury Train Ride',
        'Head Games',
        'Whisper in My Ear',
        "It's All Fun and Games (Aleta)",
        'End Game',
        'The Last Best Hope',
        'Summoner Style',
        'Gasoline',
        'The Case of the Burgled Boullogne',
        'Ishkabibble Scene Zero',
        'Ishkabibble Scene One',
        'Ishkabibble Scene Two',
        'Ishkabibble Scene Three',
        'Ishkabibble Scene Four',
        'Ishkabibble Scene Five',
        'Ishkabibble Scene Six',
        'Ishkabibble Scene Seven',
        'Ishkabibble Scene Eight',
        'Ishkabibble Scene Nine',
        'Ishkabibble Scene Twelve',
        'Ishkabibble Scene Nineteen',
        'Ishkabibble Scene Twenty-one',
        'OOC: World Building',
        'The Grand Reconstruction!',
    ]

    def __init__(self, topic=None, *args, **kwargs):
        super(Exy, self).__init__(*args, **kwargs)
        self.topics = [topic] if topic else self.default_topics

    def parse(self, response):
        yield scrapy.Request(response.url, callback=self.parse_topics)
        boards = response.selector.xpath('//a[re:test(@href, "/board/\\d+/")]')
        for board in boards:
            if not board.xpath('text()'):
                continue
            board_url = board.xpath('@href').extract_first()
            url = response.urljoin(board_url)
            yield scrapy.Request(url, callback=self.parse_topics)

    def parse_topics(self, response):
        """Queues up threads in a board for scraping."""
        topics = response.selector.xpath('//a[contains(@class, "thread-link")]')
        for topic in topics:
            if topic.xpath('text()').extract_first() not in self.topics:
                continue
            topic_url = topic.xpath('@href').extract_first()
            url = response.urljoin(topic_url)
            yield scrapy.Request(url, callback=self.parse_page)


    def parse_page(self, response):
        """Pulls out individual posts from a particular thread."""
        title = response.selector.xpath('//h1/text()').extract()[0]
        posts = response.selector.xpath('//tr[contains(@class, "post")]')
        for post in posts:
            p = Post()
            # guests first
            poster = post.xpath('td/table/tr/td/div/span/span[@class="user-guest"]/text()').extract_first()
            if not poster:
                poster = post.xpath('td/table/tr/td/div/a[contains(@class, "user-link")]/text()').extract_first()
            p['poster'] = poster
            p['content'] = post.xpath('td/table/tr/td/article/div[@class="message"]').extract()[0]
            p['post_id'] = post.xpath('@id').extract()[0]
            p['title'] = title
            yield p

        links = response.selector.xpath('//a[re:test(@href, "/thread/\\d*/.*\\?page=\\d+")]/@href').extract()
        for link in links:
            # remove this when we go to full crawling ?
            if link[:link.index('?')] not in response.url:
                continue
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse_page)
