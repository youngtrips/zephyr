#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-08
# File Name: __init__.py
# Description: 
#

import shutil
import time
import sys
import os



ZEPHYR_BIN_DIR = "ZEPHYR_BIN_DIR"
ZEPHYR_WORK_DIR = "ZEPHYR_WORK_DIR"
ZEPHYR_THEME_DIR = "ZEPHYR_THEME_DIR"
ZEPHYR_CONFIG_DIR = "ZEPHYR_CONFIG_DIR"

BIN_PATH = os.path.dirname(sys.argv[0])

def init_sketch_path(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            print 'mkdir %s failed' % (path)
            sys.exit()
    
    # init sketch path
    zephyr_path = os.path.join(path, ".zephyr")
    if not os.path.exists(zephyr_path):
        os.mkdir(zephyr_path)
    
    # copy template config
    src_config = os.path.join(BIN_PATH, 'template', 'config.py')
    dst_config = os.path.join(zephyr_path, 'config.py')
    shutil.copy(src_config, dst_config)

    # mkdir site entites
    src_html = os.path.join(BIN_PATH, 'template', 'html')
    dst_html = os.path.join(zephyr_path, 'html')
    shutil.copytree(src_html, dst_html)

    # posts path
    post_path = os.path.join(path, 'posts')
    os.mkdir(post_path)

    # pages path
    page_path = os.path.join(path, 'pages')
    os.mkdir(page_path)

    # assets path
    page_path = os.path.join(path, 'assets')
    os.mkdir(page_path)

from optparse import OptionParser

def new_post(postname, title, path):
    category = ''
    tags = ''
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    path = os.path.join(path, 'posts',
                        date.split()[0] + '-' + postname + '.md')
    sketch_header = ''
    sketch_header += '---\n'
    sketch_header += 'layout: post\n'
    sketch_header += 'title: %s\n' % title
    sketch_header += 'date: %s\n' % date
    sketch_header += 'category: %s\n' % (category)
    if len(tags) > 0:
        sketch_header += 'tags: [' + ','.join(tags) + ']\n'
    else:
        sketch_header += 'tags: \n'
    sketch_header += '---\n'
    sketch_header += '\n'
    handle = open(path, 'w')
    handle.write(sketch_header)
    handle.close()
    print 'create new post [%s].' % (path)

def rsync_site(site):
    import shlex, subprocess
    src_path = os.path.join(site.path, '.zephyr', 'html/')
    for tag, dst_path in site.config.RSYNC.iteritems():
        print 'rsync site to %s(\'%s\')......' % (tag, dst_path)
        cmdline = 'rsync -avz -e ssh %s %s' % (src_path, dst_path)
        print cmdline
        args = shlex.split(cmdline)
        p = subprocess.Popen(args)
        p.wait()

import site
def publish(path):
    zephyr_path = os.path.join(path, ".zephyr")
    if not os.path.exists(zephyr_path):
        print 'Not a sketch path'
        return
    print 'publish %s' % (path)
    mysite = site.Site(path)

    print 'start publish:'
    print 'generate html file......'
    mysite.publish()
    print 'start rsync site:'
    rsync_site(mysite)

