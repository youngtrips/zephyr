#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-04
# File Name: zephyr.py
# Description: 
#

from mako.template import Template
from mako.lookup import TemplateLookup
import markdown
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
                 layout, comment=True, publish=True, url=''):
        Node.__init__(self, url)
        self.title = title
        self.date = date
        self.time = '00:00:00'
        self.content = content
        self.author = author
        self.category = category
        self.tags = tags
        self.comment = comment
        self.publish = publish
        self.layout = layout
        self.path = os.path.join('/'.join(date.split('-')), title)
        class Foo:
            pass
        self.cate = Foo()
        self.cate.name = 'default'
        self.cate.url = '/categories/default'
        self.enable_comment = True
        print self.path

    def __cmp__(self, other):
        pass

    def __str__(self):
        return 'post<title=%s>' % title

    def set_url(self, url):
        self.url = url

    def _render(self, site, page):
        return self.layout.render(site=site,page=page,post=self)

    def generate(self, site):
        class Foo:
            pass
        page = Foo()

        page.title = self.title
        page.name = self.title
        page.url = self.url
        html = self._render(site, page)

        #generate html file
        items = self.date.split('-')
        items.append(self.title)
        path = os.path.join(site.root_path, '.zephyr')
        path = os.path.join(path, 'html')
        path = os.path.join(path, 'blog')
        for item in items:
            path = os.path.join(path, item)
            if not os.path.exists(path):
                os.mkdir(path)
        path = os.path.join(path, 'index.html')
        handle = open(path, 'w')
        handle.write(html)
        handle.close()

    @staticmethod
    def parse(site, shortname, fullname):
        if not os.path.exists(fullname):
            return None
        content = ''
        try:
            import codecs
            handle = codecs.open(fullname, mode="r", encoding="utf-8")
            content = handle.read()
            handle.close()
        except:
            return None
        HEADER_SEP = '---\n'

        pos = content.find(HEADER_SEP) + len(HEADER_SEP)
        content = content[pos:]
        pos = content.find(HEADER_SEP)
        header = content[0:pos]
        content = content[pos + len(HEADER_SEP):]
        header = yaml.load(header)

        content = markdown.markdown(content)
        items = os.path.splitext(shortname)[0].split('-')
        date = '-'.join(items[0:3])
        title = '-'.join(items[3:])

        layout = site.layout_lookup.get_template('post.html')

        post = Post(title, date, content, 'Tuz', header['category'], header['tags'], layout)
        return post

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
        self.categories = dict()
        self.tags = dict()
        self.layout_lookup = None
        self.name = 'MindEden'
        self.pages = []
        self.author = 'Tuz'
        self.enable_disqus = True
        self.enable_comment = True
        self.disqus_shortname = 'mindeden'
        self.base_url = ''
        self.base_path = ''

    def generate(self):
        for post in self.posts:
            post.generate(self)

    def publish(self):
        self._load_config()
        self._load_theme()
        self._load_posts()
        self.generate()

    def _load_config(self):
        config_path = os.path.join(self.root_path, '.zephyr')
        config_path = os.path.join(config_path, 'config')
        print config_path

    def _load_theme(self):
        theme_path = os.path.join(self.root_path, '.zephyr')
        theme_path = os.path.join(theme_path, 'themes')
        theme_path = os.path.join(theme_path, 'default')
        if not os.path.exists(theme_path):
            return False
        self.layout_lookup =  TemplateLookup(directories=[theme_path])
        #layout_post = self.layout_lookup.get_template('post.html')
        #print layout_post #.render()
        return True


    def _load_posts(self):
        for root, dirs, files in os.walk(self.root_path):
            if '.zephyr' in dirs:
                dirs.remove('.zephyr')
            for shortname in files:
                fullname = os.path.join(self.root_path, shortname)
                self._parse_post(shortname, fullname)

    def _parse_post(self, shortname, fullname):
        post = Post.parse(self, shortname, fullname)
        self._add_post(post)

    def _add_post(self, post):
        self.posts.append(post)


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

