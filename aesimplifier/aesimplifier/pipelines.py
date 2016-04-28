# -*- coding: utf-8 -*-
import re
from aesimplifier.model.topic import Topic
from aesimplifier.view.topic import topic_template, index_template


class AesimplifierPipeline(object):
    def __init__(self):
        self.topics = {}

    def close_spider(self, spider):
        topic_names = []
        for topic in self.topics.itervalues():
            filename = self._generate_file_name(topic.title)
            with open(filename, 'wb') as f:
                f.write(topic_template.render(
                    title=topic.title,
                    posts=topic.get_sorted_posts()
                ).encode('utf8'))
            topic_names.append((filename, topic.title))
        with open('index.html', 'wb') as f:
            f.write(index_template.render(
                topics=topic_names
            ).encode('utf8'))

    def process_item(self, item, spider):
        title = item['title']
        if title not in self.topics:
            self.topics[title] = Topic(title)
        self.topics[title].add_post(item)
        return item

    def _generate_file_name(self, title):
        return re.sub(r'[:\(\)\s\[\]!;]', '', title) + '.html'
