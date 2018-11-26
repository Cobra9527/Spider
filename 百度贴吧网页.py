# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib.request
import urllib.parse
import time


class Spyder(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"}
        self.url = 'https://tieba.baidu.com/f?'

    def getpage(self,url):
        req = urllib.request.Request(url, headers=self.headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode("utf-8")
        time.sleep(1)
        return html

    def writepage(self,html,page):
        filename = '第' + str(page) + '页.html'
        with open(filename, 'w', encoding="utf-8") as f:
            f.write(html)
            print('第%d页爬取成功' % page)
            print('*' * 50)

    def work(self):
        name = input('请输入要爬取的贴吧名：')
        start = int(input('请输入开始的页数：'))
        end = int(input('请输入结束的页数：'))
        key = {'kw': name}
        key = urllib.parse.urlencode(key)
        url = self.url + key
        for page in range(start, end + 1):
            pn = (page - 1) * 50
            url = url + '&pn' + str(pn)
            html = self.getpage(url)
            self.writepage(html,page)




if __name__ == '__main__':
    spyder = Spyder()
    spyder.work()
