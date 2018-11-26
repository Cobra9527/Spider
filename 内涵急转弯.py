import urllib.request
import urllib.parse
import re

class neihanSpyder(object):
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"}
        self.url = 'https://www.neihan8.com/njjzw/'
        self.page = 1

    def getpage(self,url):
        req = urllib.request.Request(url,headers=self.headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('utf-8')
        self.parsepage(html)

    def parsepage(self,html):
        p = re.compile(r'<div class="text-column-item.*?title="(.*?)">.*?class="desc">(.*?)</div>',re.S)
        r_list = p.findall(html)
        self.writepage(r_list)

    def writepage(self,r_list):
        for tup in r_list:
            with open('急转弯.txt','a',encoding='utf-8') as f:
                f.write(tup[0].strip() + '     ')
                f.write(tup[1].strip() + '\n')

    def workon(self):
        self.getpage(self.url)
        while True:
            c = input('爬取成功，是否继续（y/n）？')
            if c.strip().lower() == 'y':
                self.page += 1
                url = self.url + 'index_' + str(self.page) + '.html'
                self.getpage(url)
            else:
                print('爬取结束，欢迎下次使用')
                break



if __name__ == '__main__':
    spyder = neihanSpyder()
    spyder.workon()