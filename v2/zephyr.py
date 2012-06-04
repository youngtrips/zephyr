#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-04
# File Name: zephyr.py
# Description: 
#


class Post(object):
    def __init__(self, title, date, content, author, category, tags,
                 comment=True, publish=True):
        object.__init__(self)
        self.title = title
        self.date = date
        self.content = content
        self.author = author
        self.category = category
        self.tags = tags
        self.comment = comment
        self.publish = publish
        self.url = ''

    def __cmp__(self, other):
        pass

    def __str__(self):
        return 'post<title=%s>' % title

    def set_url(self, url):
        self.url = url


class Category(object):
    def __init__(self, name):
        object.__init__(self)
        self.name = name
        self.posts = dict()

    def add_post(self, post):
        self.posts[post.url] = post

class Tag(object):
    def __init__(self, name):
        object.__init__(self)
        self.naem = name
        self.posts = dict()
    
    def add_post(self, post):
        self.posts[post.url] = post

class Site(object):
    def __init__(self, config, author):
        object.__init__(self)
        self.config = None
        self.author = None
        self.posts = []
        self.categores = dict()
        self.tags = dict()

    def scan_sketches(self):
        pass

    def publish(self):
        pass

        
