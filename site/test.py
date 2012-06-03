#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-03
# File Name: test.py
# Description: 
#

import ConfigParser


config = ConfigParser.ConfigParser()
config.read('config')

print config.items('site')

