# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AesimplifierPipeline(object):
    def __init__(self):
        self.stuff = []

    def close_spider(self, spider):
        stuff = sorted(self.stuff, key=lambda x: x['post_id'])
        with open('bluh.html', 'wb') as f:
            f.write('<head><meta charset="UTF-8"></head><body>')
            f.write('<h1><center style="font-family: serif;">{}</center></h1>'.format(stuff[0]['title']))
            for item in stuff:
                f.write(
                    '<h2><center style="font-family: serif;">{}</center></h2>'.format(
                        item['poster'].encode('utf8')
                    )
                )
                # f.write('<center><i>{}</i></center>'.format(item['post_id']))
                f.write(
                        '<div style="width:70%; margin: 0 auto; font-family: helvetica,arial,sans-serif; line-height: 1.5;">{}</div>'.format(
                        item['content'].encode('utf8')
                    )
                )
            f.write('</body>')

    def process_item(self, item, spider):
        self.stuff.append(item)
        return item
