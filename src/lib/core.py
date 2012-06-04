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
import time

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
    def __init__(self, root_path):
        Node.__init__(self, '')
        self.root_path = root_path
        self.config = None
        self.posts = []
        self.categores = dict()
        self.tags = dict()

    def generate(self):
        pass

    def publish(self):
        self._load_config()
        self._load_theme()
        self._load_posts()

    def _load_config(self):
        config_path = os.path.join(self.root_path, '.zephyr')
        config_path = os.path.join(config_path, 'config')
        print config_path

    def _load_theme(self):
        pass

    def _load_posts(self):
        for root, dirs, files in os.walk(self.root_path):
            if '.zephyr' in dirs:
                dirs.remove('.zephyr')
            for shortname in files:
                fullname = os.path.join(self.root_path, shortname)
                self._parse_post(shortname, fullname)

    def _parse_post(self, shortname, fullname):
        print (shortname, fullname)

def init_sketch_path(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            print 'mkdir %s failed' % (path)
            sys.exit()
    
    # init sketch path
    zephyr_path = os.path.join(path, ".zephyr")
    if not os.path.exists(zephyr_path):
        os.mkdir(zephyr_path)
    
    # copy template config
    src_config = 'template/config'
    dst_config = os.path.join(zephyr_path, 'config')
    shutil.copy(src_config, dst_config)

    # copy themes
    src_themes = 'themes'
    dst_themes = os.path.join(zephyr_path, 'themes')
    shutil.copytree(src_themes, dst_themes)

    # mkdir site entites
    src_html = 'template/html'
    dst_html = os.path.join(zephyr_path, 'html')
    shutil.copytree(src_html, dst_html)

from optparse import OptionParser

def new_sketch(argv):
    if len(argv) == 0:
        sys.exit()
    parser = OptionParser()
    parser.add_option('-p', '--path', dest='sketch_path',
                      help='Create a new sketch in PATH',  metavar="PATH")
    parser.add_option('-c', '--category', dest='category',
                      help='category for sketch')
    parser.add_option('-t', '--tags', dest='tags',
                      help='tags for sketch')
    (options, args) = parser.parse_args(argv)
    sketch_path = options.sketch_path
    title = args[0]
    category = ''
    tags = []
    if sketch_path == None:
        sketch_path = os.getcwd()
    if options.category:
        category = options.category
    if options.tags:
        tags = options.tags.split()
    zephyr_path = os.path.join(sketch_path, ".zephyr")
    if not os.path.exists(zephyr_path):
        print 'Not a sketch path'
        sys.exit()

    date = time.strftime('%Y-%m-%d %H:%M:%S')
    sketch_name = date.split()[0] + '-' + title + '.md'
    sketch_path = os.path.join(sketch_path, sketch_name)
    sketch_header = ''
    sketch_header += '---\n'
    sketch_header += 'layout: post\n'
    sketch_header += 'title: \n'
    sketch_header += 'category: %s\n' % (category)
    if len(tags) > 0:
        sketch_header += 'tags: [' + ','.join(tags) + ']\n'
    else:
        sketch_header += 'tags: \n'
    sketch_header += '---\n'
    sketch_header += '\n'
    handle = open(sketch_path, 'w')
    handle.write(sketch_header)
    handle.close()
    print 'create sketch [%s].' % (sketch_path)


def publish(argv):
    path = os.getcwd()
    if len(argv) == 1:
        path = argv[0]
    zephyr_path = os.path.join(path, ".zephyr")
    if not os.path.exists(zephyr_path):
        print 'Not a sketch path'
        sys.exit()
    print 'publish %s' % (path)
    site = Site(path)
    site.publish()

