# -*- coding: utf-8 -*-


class Topic(object):
    def __init__(self, title):
        self.title = title
        self.posts = []
        self.post_ids = set()

    def add_post(self, post):
        if post['post_id'] in self.post_ids:
            return
        self.posts.append(post)
        self.post_ids.add(post['post_id'])

    def get_sorted_posts(self):
        return sorted(self.posts, key=lambda x: int(x['post_id'][5:]))

