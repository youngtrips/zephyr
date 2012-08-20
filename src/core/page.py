#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-08
# File Name: page.py
# Description: 
#

import base
import markdown
import yaml
import os

class Pageination:
    def __init__(self, base_url, total_post, page_limit):
        self.total_post = total_post
        self.page_limit = page_limit
        if self.page_limit <= 0:
            self.page_limit = 10
        ceil = lambda x, y : (x / y) + ((x % y) > 0)
        self.total_page = ceil(total_post, page_limit)
        self.current_page = 1
        self.base_url = base_url
    
    @property
    def pages(self):
        return self.total_page

    def set_current_page(self, curr):
        self.current_page = curr

    def get_current_page_posts(self):
        fr = self.page_limit * (self.current_page - 1)
        to = min(fr + self.page_limit - 1, self.total_post - 1)
        return [i for i in range(fr, to + 1)]

    def render(self, prev_word='PREV',
               next_word='NEXT',
               split_page=3,
               split_word='...'):

        if self.total_post <= 0:
            return ''

        fr = max(1, self.current_page - split_page)
        to = min(self.total_page, self.current_page + split_page)

        # prev page
        html = "<ul class='pages pagination'>"
        if self.current_page > 1:
            html += "<li><a href='%s/%d/'>" % (self.base_url, self.current_page - 1)
            html += prev_word + "</a></li>"

        # first page
        if fr > 1:
            html += "<li><a href='%s/%d/'>1</a></li>" % (self.base_url, 1)
            if fr > 2:
                html += "<li>" + split_word + "</li>"

        # internal pages
        for i in range(fr, to + 1):
            if i == self.current_page:
                html += "<li class='current active'>"
            else:
                html += "<li>"
            html += "<a href='%s/%d/'>" % (self.base_url, i)
            html += str(i) + "</a></li>"

        # last page
        if to < self.total_page:
            if to < self.total_page - 1:
                html += "<li>" + split_word + "<li>"
            html += "<li><a href='%s/%d/'>" % (self.base_url, self.total_page)
            html += str(self.total_page) + "</a></li>"
        # next page

        if self.current_page < self.total_page:
            html += "<li><a href='%s/%d/'>" % (self.base_url, self.current_page + 1)
            html += next_word + "</a></li>"
        html += "</ul>"

        return html


class Page(base.Node):
    def __init__(self, site, title, url, post_idx_list,
                 cur_page_id, cur_page_nav):
        base.Node.__init__(self, url, site)
        self.title = title
        self.posts = [site.posts[i] for i in post_idx_list]
        self.cur_page_id = cur_page_id
        self.cur_page_nav = cur_page_nav

    @property
    def pagenavigator(self):
        return self.cur_page_nav

    def generate(self):
        layout = self.parent.layout_lookup.get_template('post_list.html')
        html = layout.render(site=self.parent, page=self)
        filename = os.path.join(self.parent.path, '.zephyr', 'html',
                                self.path, 'index.html')
        base.create_file(filename, html)



class CustomPage(base.Node):
    def __init__(self, site, name, title, content, path, layout):
        base.Node.__init__(self, path, site)
        self.name = name
        self.content = content
        self.title = title
        self.layout = layout

    def generate(self):
        layout = self.parent.layout_lookup.get_template(self.layout + '.html')
        html = layout.render(site=self.parent, page=self)
        pagefile = os.path.join(self.parent.path, '.zephyr', 'html',
                                self.path, 'index.html')
        base.create_file(pagefile, html)

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
        layout = 'page'
        if header.get('layout'):
            layout = header['layout']
        name = title

        page = CustomPage(site, name, title, content, path, layout)
        return page

if __name__ == "__main__":
    pageination = Pageination('/',34, 5)
    #print pageination.render()
    pageination.set_current_page(1)
    print pageination.render()

    pageination.set_current_page(2)
    print pageination.get_current_page_posts()
    print pageination.render()

    pageination.set_current_page(3)
    print pageination.get_current_page_posts()
    print pageination.render()

