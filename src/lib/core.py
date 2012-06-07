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

BIN_PATH = os.path.dirname(sys.argv[0])

def create_file(filepath, content):
    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    print filepath
    handle = open(filepath, 'w')
    handle.write(content)
    handle.close()

class Node(object):
    def __init__(self, path, parent):
        object.__init__(self)
        self.path = path
        self.parent = parent
        self.url = ''
        if parent:
            self.url = parent.url + '/' + self.path + '/'

    def generate(self):
        pass

class Post(Node):
    def __init__(self, site, title, date, time, content, author, layout, url,
                 category=None, tags=[], enable_comment=True):
        Node.__init__(self, url, site)
        self.title = title
        self.date = date
        self.time = time
        self.content = content
        self.author = author
        self.category = category
        self.tags = tags
        self.layout = layout
        self.enable_comment = enable_comment

    @property
    def cate(self):
        return self.parent.categories[self.category]

    def __cmp__(self, other):
        pass

    def __str__(self):
        return 'post<title=%s>' % self.title

    def set_url(self, url):
        self.url = url

    def _render(self):
        class Foo:
            pass
        page = Foo()
        page.title = self.title
        page.name = self.title
        page.url = self.url
        return self.layout.render(site=self.parent,page=page,post=self)

    def generate(self):
        """
        try:
            html = self._render()
        except:
            print 'genrate post(%s) failed.' % (self.url)
            return False
        """
        html = self._render()

        #generate html file
        html_file = os.path.join(self.parent.path, '.zephyr', 'html',
                                    self.path, 'index.html')
        return create_file(html_file, html)

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
        if pos < 0:
            print 'Invalid post file(%s)' % (fullname)
            return None
        content = content[pos:]
        pos = content.find(HEADER_SEP)
        if pos < 0:
            print 'Invalid post file(%s)' % (fullname)
            return None
        header = content[0:pos]
        content = content[pos + len(HEADER_SEP):]
        header = yaml.load(header)

        items = os.path.splitext(shortname)[0].split('-')
        postfilename = '-'.join(items[3:])
        title = postfilename

        date = '-'.join(items[0:3])
        time = '00:00:00'
        layout = 'post'
        if header['date']:
            time = header['date'].strftime('%H:%M:%S')

        if header['layout']:
            layout = header['layout']
        layout = site.layout_lookup.get_template(layout+'.html')

        if header['title']:
            title = header['title']

        category = 'default'
        if header['category']:
            category = header['category']

        tags = []
        if header['tags']:
            tags = header['tags']

        enable_comment = True
        if header.get('comment'):
            enable_comment = header['comment']

        author = site.author
        url = 'blog/' + '/'.join(date.split('-')) + '/' + postfilename

        content = markdown.markdown(content)
        layout = site.layout_lookup.get_template('post.html')

        post = Post(site, title, date, time, content, author, layout, url,
                    category, tags, enable_comment)
        return post

class Category(Node):
    def __init__(self, site, name, url=''):
        Node.__init__(self, url, site)
        self.name = name
        self.posts = []

    def add_post(self, post):
        self.posts.append(post)

    def generate(self):
        class Foo:
            pass
        page = Foo()
        page.title = 'Category: ' + self.name
        page.name = self.name
        page.url = self.url
        layout = self.parent.layout_lookup.get_template("category.html")
        html = layout.render(site=self.parent, page=page, cate=self)
        filename = os.path.join(self.parent.path, '.zephyr', 'html',
                                self.path, 'index.html')
        create_file(filename, html)

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

class Page(Node):
    def __init__(self, site, name, title, content, path, layout):
        Node.__init__(self, path, site)
        self.name = name
        self.content = content
        self.title = title
        self.layout = layout

    def generate(self):
        layout = self.parent.layout_lookup.get_template(self.layout + '.html')
        html = layout.render(site=self.parent, page=self)
        pagefile = os.path.join(self.parent.path, '.zephyr', 'html',
                                self.path, 'index.html')
        create_file(pagefile, html)

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
        if pos < 0:
            print 'Invalid post file(%s)' % (fullname)
            return None
        content = content[pos:]
        pos = content.find(HEADER_SEP)
        if pos < 0:
            print 'Invalid post file(%s)' % (fullname)
            return None
        header = content[0:pos]
        content = content[pos + len(HEADER_SEP):]
        header = yaml.load(header)
        content = markdown.markdown(content)

        path = os.path.splitext(shortname)[0]
        title = path
        if header.get('title'):
            title = header['title']
        layout = 'page_index'
        if header.get('layout'):
            layout = header['layout']
        name = title

        page = Page(site, name, title, content, path, layout)
        return page


def load_config(conf):
    import imp
    obj = imp.load_source('config', conf)
    return obj

class Site(Node):
    def __init__(self, path):
        Node.__init__(self, '', None)
        self.path = path
        conf = os.path.join(self.path, '.zephyr', 'config.py')
        self.config = load_config(conf)
        self.pages = []
        self.categories = dict()
        self.posts = []
        self.layout_lookup = None
        self.enable_disqus = True
        self.url = self.config.SITE['url']

    @property
    def name(self):
        return self.config.SITE['name']
        
    @property
    def description(self):
        return self.config.SITE['description']

    @property
    def author(self):
        return self.config.AUTHOR['name']

    @property
    def pagelimit(self):
        return self.config.SITE['pagelimit']

    @property
    def disqus_shortname(self):
        return self.config.SITE['disqus_shortname']

    @property
    def theme(self):
        return self.config.SITE['theme']

    def generate(self):
        for post in self.posts:
            if post:
                post.generate()
        for name, cate in self.categories.iteritems():
            if cate:
                cate.generate()

        for page in self.pages:
            if page:
                page.generate()

        self._generate_index()


    def publish(self):
        self._load_theme()
        self._load_posts()
        self._load_pages()
        self.generate()

    def _load_theme(self):
        #theme_path = os.path.join(self.path, '.zephyr', 'themes', self.theme)
        theme_path = os.path.join(BIN_PATH, 'themes', self.theme)
        if not os.path.exists(theme_path):
            return False
        self.layout_lookup =  TemplateLookup(directories=[theme_path],
                                             input_encoding='utf-8',
                                             output_encoding='utf-8')
        # copy theme's stylesheets
        src_stylesheets = os.path.join(theme_path, 'stylesheets')
        dst_stylesheets = os.path.join(self.path,
                                       '.zephyr', 'html', 'stylesheets')
        if os.path.exists(dst_stylesheets):
            shutil.rmtree(dst_stylesheets)
        shutil.copytree(src_stylesheets, dst_stylesheets)

        # copy theme's images
        src_images = os.path.join(theme_path, 'images')
        dst_images = os.path.join(self.path,
                                       '.zephyr', 'html', 'images')
        if os.path.exists(dst_images):
            shutil.rmtree(dst_images)
        shutil.copytree(src_images, dst_images)

        # copy assets path
        src_assets = os.path.join(self.path, 'assets')
        dst_assets = os.path.join(self.path,
                                  '.zephyr', 'html', 'assets')
        if os.path.exists(dst_assets):
            shutil.rmtree(dst_assets)
        shutil.copytree(src_assets, dst_assets)
        return True

    def _load_posts(self):
        for root, dirs, files in os.walk(os.path.join(self.path, 'posts')):
            if '.zephyr' in dirs:
                dirs.remove('.zephyr')
            for shortname in files:
                fullname = os.path.join(root, shortname)
                self._parse_post(shortname, fullname)

    def _parse_post(self, shortname, fullname):
        post = Post.parse(self, shortname, fullname)
        self._add_post(post)
        self._add_category(post.category, post)

    def _load_pages(self):
        for root, dirs, files in os.walk(os.path.join(self.path, 'pages')):
            for shortname in files:
                fullname = os.path.join(root, shortname)
                self._parse_page(shortname, fullname)

    def _parse_page(self, shortname, fullname):
        page = Page.parse(self, shortname, fullname)
        if page:
            self.pages.append(page)

    def _add_post(self, post):
        self.posts.append(post)

    def _add_category(self, cate_name, post):
        cate = self.categories.get(cate_name)
        if not cate:
            url = os.path.join('categories', cate_name)
            cate = Category(self, cate_name, url)
            self.categories[cate_name] = cate
        cate.add_post(post)

    def _generate_index(self):
        filename = os.path.join(self.path, '.zephyr', 'html', 'index.html')
        layout = self.layout_lookup.get_template('page.html')
        class Foo:
            pass
        page = Foo()
        page.name = 'Home'
        page.title = 'Home'
        page.url = self.url
        html = layout.render(site=self, page=page)
        create_file(filename, html)

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
    src_config = os.path.join(BIN_PATH, 'template', 'config.py')
    dst_config = os.path.join(zephyr_path, 'config.py')
    shutil.copy(src_config, dst_config)

    # mkdir site entites
    src_html = os.path.join(BIN_PATH, 'template', 'html')
    dst_html = os.path.join(zephyr_path, 'html')
    shutil.copytree(src_html, dst_html)

    # posts path
    post_path = os.path.join(path, 'posts')
    os.mkdir(post_path)

    # pages path
    page_path = os.path.join(path, 'pages')
    os.mkdir(page_path)

from optparse import OptionParser

def new_post(postname, title, path):
    category = ''
    tags = ''
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    path = os.path.join(path, 'posts',
                        date.split()[0] + '-' + postname + '.md')
    sketch_header = ''
    sketch_header += '---\n'
    sketch_header += 'layout: post\n'
    sketch_header += 'title: %s\n' % title
    sketch_header += 'date: %s\n' % date
    sketch_header += 'category: %s\n' % (category)
    if len(tags) > 0:
        sketch_header += 'tags: [' + ','.join(tags) + ']\n'
    else:
        sketch_header += 'tags: \n'
    sketch_header += '---\n'
    sketch_header += '\n'
    handle = open(path, 'w')
    handle.write(sketch_header)
    handle.close()
    print 'create new post [%s].' % (path)

def publish(path):
    zephyr_path = os.path.join(path, ".zephyr")
    if not os.path.exists(zephyr_path):
        print 'Not a sketch path'
        return
    print 'publish %s' % (path)
    site = Site(path)
    #print site.name
    #print site.description
    #print site.author
    #print site.theme

    print 'start publish...'
    site.publish()

