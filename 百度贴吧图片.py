'''02_百度贴吧图片抓取案例.py'''
import requests
from lxml import etree
import time


class BaiduImageSpider:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.baseurl = "http://tieba.baidu.com"
        self.pageurl = "http://tieba.baidu.com/f?"


    def getPageUrl(self, params):
        res = requests.get(self.pageurl, params=params, headers=self.headers)
        res.encoding = "utf-8"
        html = res.text
        parseHtml = etree.HTML(html)
        t_list = parseHtml.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href')
        for t_link in t_list:
            t_link = self.baseurl + t_link
            self.getImageUrl(t_link)

    def getImageUrl(self, t_link):
        res = requests.get(t_link, headers=self.headers)
        res.encoding = "utf-8"
        html = res.text
        parseHtml = etree.HTML(html)
        img_list = parseHtml.xpath('//img[@class="BDE_Image"]/@src')
        for img_link in img_list:
            self.writeImage(img_link)

    def writeImage(self, img_link):
        res = requests.get(img_link, headers=self.headers)
        res.encoding = "utf-8"
        html = res.content
        filename = img_link[-12:]
        with open(filename, "wb") as f:
            f.write(html)
            time.sleep(0.5)
            print("%s下载成功" % filename)

    # 主函数
    def workOn(self):
        name = input("请输入贴吧名:")
        begin = int(input("请输入起始页:"))
        end = int(input("请输入终止页:"))

        for n in range(begin, end + 1):
            pn = (n - 1) * 50
            params = {
                "kw": name,
                "pn": str(pn)
            }
            self.getPageUrl(params)


if __name__ == "__main__":
    spider = BaiduImageSpider()
    spider.workOn()




