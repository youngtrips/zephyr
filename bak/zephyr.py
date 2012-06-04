#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-05-30
# File Name: zephyr.py
# Description: 
#

import mako
import yaml
import sys
import os

import config

class Post(object):
    def __init__(self, title, date, content, category, tags):
        object.__init__(self)
        self.category = category
        self.tags = tags
        self.date = date
        self.title = title
        self.content = content

class Node(object):
    def __init__(self, name, url):
        object.__init__(self)
        self.name = name
        self.url = url
        self.children = dict()

    def add(self, name, child):
        self.children[name] = child

    def get(self, name):
        return self.children.get(name)

    def add_child(self, name, child):
        pass

    def generate(self, output):
        path = os.path.join(output, self.url)
        if not os.path.exists(path):
            os.mkdir(path)


class PostNode(Node):
    def __init__(self, url, post):
        Node.__init__(self, post.title, url)
        self.content = post.content

    def generate(self, output):
        path = os.path.join(output, self.url)
        if not os.path.exists(path):
            os.mkdir(path)
        filename = os.path.join(path, "index.html")
        handle = open(filename, "w")
        handle.write(self.content)
        handle.close()

class CategoryNode(Node):
    def __init__(self, name, url):
        Node.__init__(self, name, url)
        self.posts = []

    def add_post(self, post):
        self.posts.append(post)

    def generate(self, output):
        path = os.path.join(output, self.url)
        if not os.path.exists(path):
            os.mkdir(path)
        ctx = ''
        for post in self.posts:
            url = os.path.join('/blog', '/'.join(post.date.split('-')))
            url = os.path.join(url, post.title)
            ctx += '<p><a href=' + url + '>' + post.title + '</a></p>'
        filename = os.path.join(path, "index.html")
        handle = open(filename, "w")
        handle.write(ctx)
        handle.close()

class TagNode(Node):
    def __init__(self, name, url):
        Node.__init__(self, name, url)
        self.posts = []

    def add_post(self, post):
        self.posts.append(post)

    def generate(self, output):
        path = os.path.join(output, self.url)
        if not os.path.exists(path):
            os.mkdir(path)
        filename = os.path.join(path, "index.html")
        handle = open(filename, "w")
        handle.close()


class Site(object):
    def __init__(self, name, url, author):
        object.__init__(self)
        self.name = name
        self.url = url
        self.author = author
        self.tree = Node('', '')

    def scan_posts(self, path):
        for root, dirs, files in os.walk(path):
            for item in files:
                fullname = os.path.join(root, item)
                self._parse_post(item, fullname)

    def _parse_post(self, shortname, fullname):
        items = os.path.splitext(shortname)[0].split('-')
        date = '-'.join(items[0:3])
        title = '-'.join(items[3:])
        print (date, title)
        #def __init__(self, title, date, content, categories, tags):
        handle = open(fullname, "r")
        lines = handle.readlines()
        handle.close()
        header = ''
        i = 0
        while i < len(lines) and lines[i] != '---\n':
            i += 1
        i += 1
        while i < len(lines) and lines[i] != '---\n':
            header += lines[i]
            i += 1
        i += 1
        content = ''
        while i < len(lines):
            content += lines[i].split('\n')[0]
            i += 1
        header = yaml.load(header)
        post = Post(title, date, content, header['category'], header['tags'])
        self._update_category_tree(post)
        self._update_tag_tree(post)
        self._update_blog_tree(post)

    def _update_category_tree(self, post):
        cate_tree = self.tree.get('categories')
        if not cate_tree:
            url = os.path.join(self.tree.url, 'categories')
            cate_tree = Node("categories", url)
            self.tree.children['categories'] = cate_tree
        cate = cate_tree.get(post.category)
        if cate == None:
            url = os.path.join(cate_tree.url, post.category)
            cate = CategoryNode(post.category, url)
            cate_tree.children[cate.name] = cate
        cate.add_post(post)

    def _update_tag_tree(self, post):
        tag_tree = self.tree.get('tags')
        if not tag_tree:
            url = os.path.join(self.tree.url, 'tags')
            tag_tree = Node('tags', url)
            self.tree.add('tags', tag_tree)
        for tagname in post.tags:
            tag = tag_tree.get(tagname)
            if not tag:
                url = os.path.join(tag_tree.url, tagname)
                tag = TagNode(tagname, url)
                tag_tree.add(tagname, tag)
            tag.add_post(post)

    def _update_blog_tree(self, post):
        blog_tree = self.tree.get('blog')
        if not blog_tree:
            url = os.path.join(self.tree.url, 'blog')
            blog_tree = Node('blog', url)
            self.tree.add('blog', blog_tree)

        items = post.date.split('-')
        cur_node = blog_tree
        for item  in items:
            new_node = cur_node.get(item)
            if not new_node:
                new_node = Node(item, os.path.join(cur_node.url, item))
                cur_node.add(item, new_node)
            cur_node = new_node
        url = os.path.join(cur_node.url, post.title)
        postnode = PostNode(url, post)
        cur_node.add(postnode.name, postnode)

    def generate(self, output):
        def _generate(root):
            root.generate(output)
            for key in root.children.keys():
                child = root.get(key)
                _generate(child)
        _generate(self.tree)

def main():
    site = Site('MindEden', 'http://127.0.0.1', 'Tuz')
    site.scan_posts(config.site_path)
    site.generate(config.html_path)

if __name__ == "__main__":
    main()

