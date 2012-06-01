#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-01
# File Name: test.py
# Description: 
#


from mako.template import Template
from mako.lookup import TemplateLookup

mylookup = TemplateLookup(directories=['.'])
tpl = mylookup.get_template("page.html")
print tpl.render()

