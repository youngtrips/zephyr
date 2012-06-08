#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-08
# File Name: site.py
# Description: 
#

class Site(Node):
    def __init__(self, path):
        Node.__init__(self, '', None)
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

        for page in self.pages:
            if page:
                page.generate()

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
        shutil.copytree(src_stylesheets, dst_stylesheets)

        # copy theme's images
        src_images = os.path.join(theme_path, 'images')
        dst_images = os.path.join(self.path,
                                       '.zephyr', 'html', 'images')
        if os.path.exists(dst_images):
            shutil.rmtree(dst_images)
        shutil.copytree(src_images, dst_images)

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
        page = Page.parse(self, shortname, fullname)
        if page:
            self.pages.append(page)

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
        filename = os.path.join(self.path, '.zephyr', 'html', 'index.html')
        layout = self.layout_lookup.get_template('page.html')
        class Foo:
            pass
        page = Foo()
        page.name = 'Home'
        page.title = 'Home'
        page.url = self.url

        cmpfunc = lambda p1, p2 : cmp(p2.timestamp, p1.timestamp)
        self.posts.sort(cmp=cmpfunc)
        html = layout.render(site=self, page=page)
        create_file(filename, html)

