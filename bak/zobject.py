#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-03
# File Name: zobject.py
# Description: 
#

class Node(object):
    def __init__(self, name, url):
        object.__init__(self)
        self.name = name
        self.url = url

    def generate(self):
        pass


class Post(Node):
    def __init__(self, title, date, author, content, category, tags, url):
        Node.__init__(self, title, url)
        self.title = title
        self.date = date
        self.author = author
        self.content = content
        self.category = category
        self.tags = tags


class Category(Node):
    def __init__(self, name, url):
        Node.__init__(self, name, url)



class Tag(Node):
    def __init__(self, name, url):
        Node.__init__(self, name, url)


class Site(Node):
    def __init__(self, name, base_url):
        Node.__init__(self, name, base_url)
        self.posts = []
        self.categoris = dict()
        self.tags = dict()



