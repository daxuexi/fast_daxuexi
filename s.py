#-*- coding:UTF-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import time
from collections import OrderedDict


# 定义爬虫类
class Spider():
    def __init__(self):
        self.url = 'http://news.cyol.com/node_67071.htm'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        r = requests.get(self.url, headers=self.headers)
        r.encoding = r.apparent_encoding
        self.html = r.text
        # print(self.html)

    def BeautifulSoup_find(self,class_name):
        '''用BeautifulSoup解析'''

        soup = BeautifulSoup(self.html, 'lxml')
        titles = soup.find_all(attrs={'class': class_name})
        link_list = []
        for each in titles:
            #print(each['href'])
            link_list.append(str(each['href']))
        return link_list
class Spider_onepage():
    def __init__(self,url):
        self.url = url
        print(url)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        r = requests.get(self.url, headers=self.headers)
        r.encoding = r.apparent_encoding
        self.html = r.text
        # print(self.html)

    def BeautifulSoup_find(self,class_name):
        '''用BeautifulSoup解析'''

        soup = BeautifulSoup(self.html, 'lxml')
        title = soup.title.string
        print(title)
        titles = soup.find_all(attrs={'class': class_name})
        print(type(titles))
        final_title = re.findall('.*<h1>(.*)</h1>.*',str(titles))
        print('titles:{}'.format(final_title))
        return final_title[0]


def get_title_ulrs():
    spider = Spider()
    link_list = spider.BeautifulSoup_find('transition')
    real_h5_links = OrderedDict()
    for l in link_list:
        s = l.split('/')
        id = s[-2]
        if 'h5.cyol.com' not in s:
            continue

        real_h5_links[id] = ['http://h5.cyol.com/special/daxuexi/{}/images/end.jpg'.format(id),l]
    print(real_h5_links)
    return real_h5_links


def generate_html(h5_links):
    newest = list(h5_links.items())[0][1]
    new_page = Spider_onepage(newest[-1])
    title = new_page.BeautifulSoup_find('cont_h')
	
    url = newest[1]
    download_img(url)
    make_html(title)


def make_html(title):
    with open('index.html', 'w', encoding='utf-8') as f:
        message = '<html> <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><meta http-equiv="pragma" content="no-cache"><meta http-equiv="expires" content="Tue, 01 Jan 2013 00:00:00 GMT"><meta http-equiv="expires" content="0"><meta http-equiv="Cache-Control" content="no-cache,must-revalidate"><head><title>{}</title></head> <body> <img style="position:absolute;left:0px;top:0px;width:100%;height:100%;z-Index:-1;" src="new.jpg" /> </body>'.format(
            title)
        f.write(message)


def download_img(img_url):
    print(img_url)
    header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    r = requests.get(img_url, headers=header, stream=True)
    print(r.status_code)
    if r.status_code == 200:
        open('new.jpg', 'wb').write(r.content) 


if __name__ == '__main__':
    links = get_title_ulrs()
    generate_html(links)
