from bs4 import BeautifulSoup
import re
import urllib.error
from fake_useragent import UserAgent
import requests
import json


def main(keyword):
    baseurl = "https://www.mercari.com/jp/search/?keyword="+keyword
    last={}
    # 爬取
    datalist = getData(baseurl)
    #保存为字典
    for index, item in enumerate(datalist):
        dic = {'title': item[0], 'picurl': item[1], 'url': item[2], 'price': item[3],'lover':item[4]}
        last[str(index)]=dic
    str(last)
    return str(last)

# 正则
findtitle = re.compile(r'<h3 class="items-box-name font-2">(.*?)</h3>')  # 标题
findimgsrc = re.compile(r'class="lazyload" data-src="(.*?)"/>')
findprice = re.compile(r'<div class="items-box-price font-5">(.*?)</div>')
findliker = re.compile(r'<span>(\d*?)</span>')
findlink = re.compile(r'<a href="(.*?)">')


def getData(baseurl):
    datalist = []
    html = askURL(baseurl)
    # print(html)
    bs = BeautifulSoup(html, "html.parser")
    for item in bs.findAll('section', class_="items-box"):
        data = []
        item = str(item)

        # 获取标题
        title = re.findall(findtitle, item)[0]
        title = re.sub("'","#u0027",title)
        title = re.sub('"',"#u0022",title)
        title = re.sub(u'\xa0',u' ',title)
        title = re.sub(u'\u3000',u' ',title)
        data.append(title)
        # 获取图片src
        imgsrc = re.findall(findimgsrc, item)[0]
        data.append(imgsrc)
        # 获取链接
        link = re.findall(findlink, item)[0]
        data.append("https://www.mercari.com"+link)
        # 获取价钱
        price = re.findall(findprice, item)[0]
        data.append(price)
        # 获取关注
        liker = re.findall(findliker, item)
        if len(liker) == 0:
            data.append('0')
        else:
            data.append(liker[0])

        datalist.append(data)

    return datalist


def askURL(url):
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random
    }
    html = ""
    try:
        response = requests.get(url, headers=headers)
        html = response.content.decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


""" if __name__ == "__main__":
    # keyword=input('検索ワードを入力してください')
    keyword = 'iphone'
    main(keyword) """
 
def search(keyword):
    return main(keyword)
