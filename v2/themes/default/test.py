#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-01
# File Name: test.py
# Description: 
#


from mako.template import Template
from mako.lookup import TemplateLookup


class Foo:
    pass


site = Foo()
post = Foo()
page = Foo()


site.name = "MindEden"
site.author = "Tuz"
site.url = "http://mindeden.com"
site.pagelimit = 10
site.pages = []
site.categories = []
site.posts = []
site.enable_disqus = True
site.disqus_shortname = "mindeden"

page.title = "Home"
page.name = "Home"
page.url = site.url

#site.pages.append(page)

cate = Foo()
cate.name = "default"
cate.url = site.url + "/categories/" + cate.name

site.categories.append(cate)

post.title = "Welcome to MindEden"
post.date = "2012-06-01"
post.time = "10:55:02"
post.cate = cate
post.url = site.url + "/post/2012/06/01/welcome-to-mindeden/"
post.content = "Welcome to MindEden, it's coming soon!!!"
post.enable_comment = True


page.title = post.title

site.posts.append(post)

mylookup = TemplateLookup(directories=['.'])
tpl = mylookup.get_template("post.html")
print tpl.render(site=site, post=post, page=page)

