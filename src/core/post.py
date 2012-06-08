#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-08
# File Name: post.py
# Description: 
#

import markdown
import logging
import yaml
import time
import base
import os

class Post(base.Node):
    def __init__(self, site, title, publish_datetime,
                 content, author, url, category='default',
                 tags=[], layout=None,
                 enable_comment=True):
        base.Node.__init__(self, url, site)
        self.title = title
        self.publish_datetime = publish_datetime
        self.content = content
        self.author = author
        self.category = category
        self.tags = tags
        self.layout = layout
        self.enable_comment = enable_comment
        self.timestamp = 0

    @property
    def datetime(self):
        return self.publish_datetime

    @property
    def cate(self):
        return self.parent.categories[self.category]

    def __cmp__(self, other):
        return cmp(other.timestamp, self.timestamp)

    def __str__(self):
        return 'post<title=%s, timestamp=%d>' % (self.title, self.timestamp)

    def _render(self):
        class Foo:
            pass
        page = Foo()
        page.title = self.title
        page.name = self.title
        page.url = self.url
        return self.layout.render(site=self.parent,page=page,post=self)

    def generate(self):
        html = self._render()

        #generate html file
        html_file = os.path.join(self.parent.path,
                                 '.zephyr',
                                 'html',
                                 self.path,
                                 'index.html')
        return base.create_file(html_file, html)

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
            logging.info('open file[%s] failed.' % fullname)
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

        timestamp = time.mktime(header['date'].utctimetuple())

        date = '-'.join(items[0:3])
        timeval = '00:00:00'
        layout = 'post'
        if header['date']:
            timeval = header['date'].strftime('%H:%M:%S')

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
        if header.get('comments'):
            enable_comment = header['comments']

        author = site.author
        url = os.path.join('blog', '/'.join(date.split('-')), postfilename)

        content = markdown.markdown(content)
        post = Post(site, title, date + ' '+ timeval,
                    content, author, url,
                    category, tags, layout,
                    enable_comment)
        post.timestamp = timestamp
        return post

