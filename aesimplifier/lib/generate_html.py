# -*- coding: utf-8 -*-
import json
import os
import re
from aesimplifier.model.topic import Topic
from aesimplifier.view.templates import topic_template, index_template

DIST = 'dist'


def generate_html(content_file):
    """Given the output json file, generate HTML pages for the topics crawled
    as well as an index in the dist directory."""
    topic_names = []
    topics = {}
    with open(content_file, 'r') as infile:
        posts = json.load(infile)
        for post in posts:
            if post['title'] not in topics:
                topics[post['title']] = Topic(post['title'])
            topics[post['title']].add_post(post)

    for topic in topics.itervalues():
        _write_topic(topic)
        topic_names.append(topic.title)

    with open(os.path.join(DIST, 'index.html'), 'wb') as f:
        f.write(index_template.render(topics=topic_names).encode('utf8'))


def _write_topic(topic):
    filename = _generate_file_name(topic.title)
    with open(os.path.join(DIST, filename), 'wb') as f:
        f.write(topic_template.render(
            title=topic.title,
            posts=topic.get_sorted_posts()
        ).encode('utf8'))


def _generate_file_name(title):
    return re.sub(r'[:\(\)\s\[\]!;\']', '', title) + '.html'
