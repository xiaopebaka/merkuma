#-*- codeing = utf-8 -*-
#@Author: m.kaku
#@Date: 2020-12-30 15:05:59
#@LastEditTime: 2021-01-06 00:54:44

from bs4 import BeautifulSoup
import re
import urllib.error
from fake_useragent import UserAgent
import requests


def main(keyword):
    baseurl = "https://fril.jp/search/"+keyword
    last={}
    # 爬取
    datalist = getData(baseurl)
    # 保存为字典
    for index, item in enumerate(datalist):
        dic = {'title': item[0], 'picurl': item[2], 'url': item[3], 'price': item[1]}
        last[str(index)]=dic
    return str(last)


def getData(baseurl):
    datalist = []
    for i in range(0,4):
        html = askURL(baseurl+"/page/"+str(i)+"?order=desc&sort=relevance")
        bs = BeautifulSoup(html, "html.parser")
        for item in bs.findAll('div', class_="item"):
            data = []
            #标题
            title = item.select("div > div.item-box__text-wrapper > p > a > span")[0].get_text()
            title = re.sub("'","#u0027",title)
            title = re.sub('"',"#u0022",title)
            title = re.sub(u'\xa0',u' ',title)
            title = re.sub(u'\u3000',u' ',title)
            data.append(title)
            #价格
            price=item.select("div > div.item-box__text-wrapper > div:nth-child(3) > p > span:nth-child(2)")[0].get_text()
            data.append(price)
            #图片
            imgsrc=item.img
            data.append((imgsrc['data-original']))
            #连接
            link=item.a
            data.append(link['href'])


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
    #keyword=input('検索ワードを入力してください')
    main("macbook")
    print('処理終了') """

def search(keyword):
    return main(keyword)