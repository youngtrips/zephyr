#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-08
# File Name: base.py
# Description: 
#

import logging
import os

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

def create_file(fullfilename, content):
    dirname = os.path.dirname(fullfilename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    #logging.info('generate file: %s' % fullfilename)
    print 'generate file: %s' % (fullfilename)
    handle = open(fullfilename, 'w')
    handle.write(content)
    handle.close()

