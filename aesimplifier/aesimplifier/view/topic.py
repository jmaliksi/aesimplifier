# -*- coding: utf-8 -*-
from jinja2 import Environment, PackageLoader


env = Environment(loader=PackageLoader('aesimplifier', 'view'))
topic_template = env.get_template('topic.html')
