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

class Site(object):
    def __init__(self, config):
        object.__init__(self)
        self.config = None
        self.posts = []
        self.categores = dict()
        self.tags = dict()

    def scan_sketches(self):
        pass

    def publish(self):
        pass

        





from optparse import OptionParser
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--init", dest="sketch_path",
                      help="initialize path for sketches")
    parser.add_option("-p", "--published",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

    (options, args) = parser.parse_args()



