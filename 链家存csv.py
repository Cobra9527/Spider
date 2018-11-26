import requests
import time
import re
import csv

class Lianjia(object):

    def __init__(self):
        self.url = 'https://qd.lianjia.com/ershoufang/'
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"}
        self.number = 1


    def getpage(self):
        url = self.url + str(self.number)
        respond = requests.get(url,headers=self.headers)
        respond.encoding = 'utf-8'
        html = respond.text
        self.readpage(html)

    def readpage(self,html):
        p = re.compile(r'<div class="houseInfo".*?data-el="region">(.*?)</a>(.*?)</div>.*?<div class="totalPrice"><span>(.*?)</span>.*?<span>(.*?)</span>',re.S)
        li = p.findall(html)
        self.writecsv(li)


    def writecsv(self,li):
        with open('链家.csv','a',newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['房源名称','房源详情','总价','单价'])
            for house in li:
                name = house[0].strip()
                info = house[1].strip()
                totalprice = float(house[2].strip()) * 10000
                price = house[3].strip()
                writer.writerow([name,info,totalprice,price])
            print('存入CSV成功')


    def workon(self):
        self.getpage()
        self.number += 1
        while True:
            go = input('爬取成功，是否继续（y/n）')
            if go == 'n':
                print('程序结束，感谢使用')
                break
            else:
                self.getpage()
                self.number += 1
                time.sleep(1)

if __name__ == '__main__':
    lianjia = Lianjia()
    lianjia.workon()