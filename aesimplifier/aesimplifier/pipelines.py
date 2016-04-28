# -*- coding: utf-8 -*-
from aesimplifier.model.topic import Topic
from aesimplifier.view.topic import topic_template


class AesimplifierPipeline(object):
    def __init__(self):
        self.topics = {}

    def close_spider(self, spider):
        for topic in self.topics.itervalues():
            with open(topic.title + '.html', 'wb') as f:
                f.write(topic_template.render(
                    title=topic.title,
                    posts=topic.get_sorted_posts()
                ).encode('utf8'))
               
    def process_item(self, item, spider):
        title = item['title']
        if title not in self.topics:
            self.topics[title] = Topic(title)
        self.topics[title].add_post(item)
        return item
