# -*- coding: utf-8 -*-
from aesimplifier.model.topic import Topic


class AesimplifierPipeline(object):
    def __init__(self):
        self.topics = {}

    def close_spider(self, spider):
        for topic in self.topics.itervalues():
            with open(topic.title + '.html', 'wb') as f:
                f.write('<head><meta charset="UTF-8"></head><body>')
                f.write(
                    '<h1><center style="font-family: serif;">{}</center></h1>'.format(topic.title)
                )
                for post in topic.get_sorted_posts():
                    f.write(
                        '<h2><center style="font-family: serif;">{}</center></h2>'.format(
                            post['poster'].encode('utf8')
                        )
                    )
                    f.write(
                            '<div style="width:80%; margin: 0 auto; font-family: helvetica,arial,sans-serif; line-height: 1.5;">{}</div>'.format(
                            post['content'].encode('utf8')
                        )
                    )
                f.write('</body>')

    def process_item(self, item, spider):
        title = item['title']
        if title not in self.topics:
            self.topics[title] = Topic(title)
        self.topics[title].add_post(item)
        return item
