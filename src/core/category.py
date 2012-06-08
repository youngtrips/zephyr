#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-08
# File Name: category.py
# Description: 
#


import shutil
import base
import page
import os

class Category(base.Node):
    def __init__(self, site, name, url=''):
        base.Node.__init__(self, url, site)
        self.name = name
        self.posts = []

    def add_post(self, post):
        self.posts.append(post)

    def generate(self):
        self.posts.sort()
        base_url = self.url + "/page"
        pageination = page.Pageination(base_url, len(self.posts),
                                       self.parent.pagelimit)
        for cur_page_id in range(1, pageination.pages + 1):
            pageination.set_current_page(cur_page_id)
            post_idx_list = pageination.get_current_page_posts()
            cur_page_nav = pageination.render()
            self.generate_page(cur_page_id, cur_page_nav, post_idx_list)

        html = os.path.join(self.parent.path, '.zephyr', 'html',
                            self.path, 'index.html')

        firstpage = os.path.join(self.parent.path, '.zephyr', 'html',
                                 self.path, 'page', '1', 'index.html')
        shutil.copy(firstpage, html)

    def generate_page(self, cur_page_id, cur_page_nav, post_idx_list):
        title = 'Category &raquo; ' + self.name
        url = os.path.join(self.path, 'page', str(cur_page_id))
        cur_page = page.Page(self.parent, title, url, post_idx_list,
                             cur_page_id, cur_page_nav)
        cur_page.generate()
        
