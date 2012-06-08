#-*- coding: utf-8 -*-

# Author: youngtrips(youngtrips@gmail.com)
# Created Time:  2012-06-08
# File Name: page.py
# Description: 
#

class Pageination:
    def __init__(self, total_post, page_limit):
        self.total_post = total_post
        self.page_limit = page_limit
        if self.page_limit <= 0:
            self.page_limit = 10
        ceil = lambda x, y : (x / y) + ((x % y) > 0)
        self.total_page = ceil(total_post, page_limit)
        self.current_page = 1
    
    def set_current_page(self, curr):
        self.current_page = curr

    def get_current_page_posts(self):
        fr = self.page_limit * (self.current_page - 1)
        to = min(fr + self.page_limit - 1, self.total_post - 1)
        return [i for i in range(fr, to + 1)]

    def render(self, prev_word='PREV',
               next_word='NEXT',
               split_page=3,
               split_word='...'):

        if self.total_post <= 0:
            return ''

        fr = max(1, self.current_page - split_page)
        to = min(self.total_page, self.current_page + split_page)

        # prev page
        html = ""
        if self.current_page > 1:
            html += "<li><a href='prev' href='#'>" + prev_word + "</a></li>"

        # first page
        if fr > 1:
            html += "<li><a href='#'>1</a></li>"
            if fr > 2:
                html += "<li>" + split_word + "</li>"

        # internal pages
        for i in range(fr, to + 1):
            if i == self.current_page:
                html += "<li class='current'>"
            else:
                html += "<li>"
            html += "<a href='#'>" + str(i) + "</a></li>"

        # last page
        if to < self.total_page:
            if to < self.total_page - 1:
                html += "<li>" + split_word + "<li>"
            html += "<li><a href='#'>" + str(self.total_page) + "</a></li>"
        # next page

        if self.current_page < self.total_page:
            html += "<li><a href='next' href='#'>" + next_word + "</a></li>"

        return html


if __name__ == "__main__":
    pageination = Pageination(34, 5)
    #print pageination.render()
    pageination.set_current_page(1)
    print pageination.get_current_page_posts()

    pageination.set_current_page(2)
    print pageination.get_current_page_posts()

    pageination.set_current_page(3)
    print pageination.get_current_page_posts()


