#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-04
# File Name: zephyr.py
# Description: 
#

import markdown
import mako
import yaml
import sys
import os
import shutil

class Node(object):
    def __init__(self, url):
        object.__init__(self)
        self.url = url

    def generate(self):
        pass

class Post(Node):
    def __init__(self, title, date, content, author, category, tags,
                 comment=True, publish=True, url=''):
        Node.__init__(self, url)
        self.title = title
        self.date = date
        self.content = content
        self.author = author
        self.category = category
        self.tags = tags
        self.comment = comment
        self.publish = publish

    def __cmp__(self, other):
        pass

    def __str__(self):
        return 'post<title=%s>' % title

    def set_url(self, url):
        self.url = url

    def generate(self):
        pass

class Category(Node):
    def __init__(self, name, url=''):
        Node.__init__(self, url)
        self.name = name
        self.posts = dict()

    def add_post(self, post):
        self.posts[post.url] = post

    def generate(self):
        pass

class Tag(Node):
    def __init__(self, name, url=''):
        Node.__init__(self, url)
        self.naem = name
        self.posts = dict()
    
    def add_post(self, post):
        self.posts[post.url] = post

    def generate(self):
        pass

class Author(object):
    def __init__(self, name, mail):
        object.__init__(self)
        self.name = name
        self.mail = mail

class Config(object):
    def __init__(self, conf):
        object.__init__(self)
        self._parse(conf)

    def _parse(self, conf):
        pass

class Site(Node):
    def __init__(self, config):
        Node.__init__(self, '')
        self.config = None
        self.posts = []
        self.categores = dict()
        self.tags = dict()
        self.root_path = ''

    def generate(self):
        pass

    def scan_sketches(self):
        pass

    def publish(self):
        for post in self.posts:
            post.generate()

        for key in self.categores.keys():
            cate = self.categores[key]
            cate.generate()

        for key in self.tags.keys():
            tag = self.tags[key]
            tag.generate()
        self.generate()


def init_sketch_path(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            print 'mkdir %s failed' % (path)
            sys.exit()
    
    # init sketch path
    zephyr_path = os.path.join(path, ".zephyr")
    os.mkdir(zephyr_path)
    
    # copy template config
    src_config = 'template/config'
    dst_config = os.path.join(zephyr_path, 'config')
    shutil.copy(src_config, dst_config)

    # copy themes
    src_themes = 'themes'
    dst_themes = os.path.join(zephyr_path, 'themes')
    shutil.copytree(src_themes, dst_themes)

