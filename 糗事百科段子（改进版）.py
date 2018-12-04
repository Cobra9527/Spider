import requests
from lxml import etree
import time

class Qiushi:

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"}
        self.pageurl = 'https://www.qiushibaike.com/8hr/page/'
        self.duanziurl = 'https://www.qiushibaike.com/article/'
        self.number = 1

    def getPage(self):
        url = self.pageurl + str(self.number)
        res = requests.get(url,headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        parseHtml = etree.HTML(html)
        p_list = parseHtml.xpath('//div[@id="content-left"]/div/@id')
        p_list = set(p_list)
        for p in p_list:
            p = p.split('_')[2]
            url = self.duanziurl + p
            self.getDuanzi(url)

    def getDuanzi(self,url):
        res = requests.get(url,headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        parseHtml = etree.HTML(html)
        name = parseHtml.xpath('//div[@class="author clearfix"]/a/h2')
        if len(name) == 0:
            name = '匿名用户'
        else:
            name = name[0].text.strip()
        duanzi = parseHtml.xpath('//div[@class="content"]')
        if duanzi[0].text is None:
            duanzi = '图片段子'
        else:
            duanzi = duanzi[0].text.strip()
            duanzi2 = parseHtml.xpath('//div[@class="content"]/br')
            for s in duanzi2:
                if s.tail is not None:
                    duanzi += s.tail.strip()
        laugh = parseHtml.xpath('//span[@class="stats-vote"]/i')
        ping = parseHtml.xpath('//span[2]/i')
        if len(laugh) == 0:
            laugh = 0
        else:
            laugh = laugh[0].text
        if len(ping) == 0:
            ping = 0
        else:
            ping = ping[0].text
        dic = {
            '用户名':name,
            '段子':duanzi,
            '好笑':laugh,
            '评论':ping
         }
        self.writeDuanzi(dic)

    def writeDuanzi(self,dic):
        filename = '糗事百科段子.txt'
        with open(filename,'a',encoding='utf-8') as f:
            f.write(str(dic))
            f.write('\n')
        print('写入成功')

    def workOn(self):
        print('欢迎使用，程序开始运行!')
        while True:
            order = input('是否继续（y/n）？')
            if order == 'n':
                print('欢迎下次使用！')
                break
            else:
                self.getPage()
                self.number += 1
                time.sleep(1)


if __name__ == '__main__':
    spider = Qiushi()
    spider.workOn()