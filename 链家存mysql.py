import requests
import time
import re
import pymysql

class Lianjia(object):

    def __init__(self):
        self.url = 'https://qd.lianjia.com/ershoufang/'
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"}
        self.number = 1
        self.db = pymysql.connect("localhost","root","888888",charset="utf8")
        self.cursor = self.db.cursor()

    def getpage(self):
        url = self.url + str(self.number)
        respond = requests.get(url,headers=self.headers)
        respond.encoding = 'utf-8'
        html = respond.text
        self.readpage(html)

    def readpage(self,html):
        p = re.compile(r'<div class="houseInfo".*?data-el="region">(.*?)</a>(.*?)</div>.*?<div class="totalPrice"><span>(.*?)</span>.*?<span>(.*?)</span>',re.S)
        li = p.findall(html)
        self.writemysql(li)


    def writemysql(self,li):
        c_db = 'create database if not exists lianjia character set utf8'
        u_db = 'use lianjia'
        c_tab = 'create table if not exists houseinfo (id int primary key auto_increment,housename varchar(50),info varchar(100),totalprice int,price varchar(50))charset=utf8'

        self.cursor.execute(c_db)
        self.cursor.execute(u_db)
        self.cursor.execute(c_tab)
        ins = 'insert into houseinfo(housename,info,totalprice,price) values(%s,%s,%s,%s)'
        for house in li:
            name = house[0].strip()
            info = house[1].strip()
            totalprice = float(house[2].strip()) * 10000
            price = house[3].strip()
            L = [name,info,totalprice,price]
            self.cursor.execute(ins,L)
            self.db.commit()
            print('存入数据库成功')


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