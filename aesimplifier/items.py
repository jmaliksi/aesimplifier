# -*- coding: utf-8 -*-
import scrapy


class Post(scrapy.Item):
    poster = scrapy.Field()
    content = scrapy.Field()
    post_id = scrapy.Field()
    title = scrapy.Field()
