# -*- coding: utf-8 -*-
from collections import namedtuple


class Topic(object):
    def __init__(self, title):
        self.title = title
        self.posts = []
        self.post_ids = set()

    def add_post(self, post):
        if post['post_id'] in self.post_ids:
            return
        self.posts.append(Post(
            poster=post['poster'].encode('utf8'),
            content=post['content'].encode('utf8'),
            post_id=post['post_id'],
        ))
        self.post_ids.add(post['post_id'])

    def get_sorted_posts(self):
        return sorted(self.posts, key=lambda x: int(x.post_id[5:]))


Post = namedtuple(
    'Post', [
        'poster',
        'content',
        'post_id',
    ]
)
