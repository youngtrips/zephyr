#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-08
# File Name: site.py
# Description: 
#

from mako.template import Template
from mako.lookup import TemplateLookup
import markdown
import shutil
import yaml
import page
import base
from post import Post
from category import Category
import sys
import os

BIN_PATH = os.path.dirname(sys.argv[0])

def load_config(conf):
    import imp
    obj = imp.load_source('config', conf)
    return obj

class Site(base.Node):
    def __init__(self, path):
        base.Node.__init__(self, '', None)
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
        self.posts.sort()
        for post in self.posts:
            if post:
                post.generate()

        for name, cate in self.categories.iteritems():
            if cate:
                cate.generate()

        for custom_page in self.pages:
            if custom_page:
                custom_page.generate()

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
                                             output_encoding='utf-8',
                                             imports=['from lib.common import truncate_html'])
        # copy theme's stylesheets
        src_stylesheets = os.path.join(theme_path, 'stylesheets')
        dst_stylesheets = os.path.join(self.path,
                                       '.zephyr', 'html', 'stylesheets')
        if os.path.exists(dst_stylesheets):
            shutil.rmtree(dst_stylesheets)

        """
        shutil.copytree(src_stylesheets, dst_stylesheets)

        # copy theme's images
        src_images = os.path.join(theme_path, 'images')
        dst_images = os.path.join(self.path,
                                       '.zephyr', 'html', 'images')

        if os.path.exists(dst_images):
            shutil.rmtree(dst_images)
        shutil.copytree(src_images, dst_images)
        """

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
        custompage = page.CustomPage.parse(self, shortname, fullname)
        if custompage:
            self.pages.append(custompage)

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
        self._generate_post_list()
        index = os.path.join(self.path, '.zephyr', 'html', 'index.html')
        firstpage = os.path.join(self.path, '.zephyr', 'html', 'page', '1',
                                 'index.html')
        shutil.copy(firstpage, index)

    def _generate_post_list(self):
        self.posts.sort()
        base_url = self.url + "/page"
        pageination = page.Pageination(base_url, len(self.posts), self.pagelimit)
        for cur_page_id in range(1, pageination.pages + 1):
            pageination.set_current_page(cur_page_id)
            post_idx_list = pageination.get_current_page_posts()
            cur_page_nav = pageination.render()
            self._generate_postlist_page(cur_page_id, cur_page_nav, post_idx_list)


    def _generate_postlist_page(self, cur_page_id, cur_page_nav,
                                post_idx_list):
        title = 'Home'
        url = os.path.join('page', str(cur_page_id))
        cur_page = page.Page(self, title, url, post_idx_list,
                             cur_page_id, cur_page_nav)
        cur_page.generate()

