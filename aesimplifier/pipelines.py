# -*- coding: utf-8 -*-
import os
import re
from scrapy.exceptions import DropItem
from aesimplifier.model.topic import Topic
from aesimplifier.view.templates import topic_template, index_template

DIST = 'dist'


class AesimplifierPipeline(object):
    def __init__(self):
        self.post_ids = set()

    def process_item(self, item, spider):
        if item['post_id'] in self.post_ids:
            raise DropItem('Duplicate {}'.format(item['post_id']))
        return item
