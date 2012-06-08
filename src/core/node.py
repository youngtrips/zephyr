#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-08
# File Name: node.py
# Description: 
#

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

