from selenium import webdriver
from lxml import etree
import time

# 把Chrome设置无界面浏览器
opt = webdriver.ChromeOptions()
opt.set_headless()

driver = webdriver.Chrome(options=opt)
driver.get("https://www.douyu.com/directory/all")
i = 1

while True:
    # 解析(driver.page_source)
    # 获取主播名称 和 观众人数
    parseHtml = etree.HTML(driver.page_source)
    names = parseHtml.xpath('//div[@id="live-list-content"]//span[@class="dy-name ellipsis fl"]')
    numbers = parseHtml.xpath('//div[@id="live-list-content"]//span[@class="dy-num fr"]')

    for name, number in zip(names, numbers):
        print("\t主播名称：%s \t观众人数：%s" %(name.text.strip(), number.text.strip()))
    print("第%d页爬取成功" % i)
    i += 1
    # 判断是否需要点击下一页
    if driver.page_source.find("shark-pager-disable-next") == -1:
        driver.find_element_by_class_name("shark-pager-next").click()
        time.sleep(1)
    else:
        break

print("一共爬取了%d页" % i)
