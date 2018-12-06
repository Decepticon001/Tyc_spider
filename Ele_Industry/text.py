# -*- coding: utf-8 -*-

import urllib.request
import requests
import re
from lxml import etree
# import xlrd

class jsds(object):
    def __init__(self):
        self.url = 'http://pub.jsds.gov.cn/col/col48038/index.html'
        # self.url = 'http://tieba.baidu.com/f?kw={}'.format(name)
        self.headers = {
            # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0',
            # 'Referer': 'http://pub.jsds.gov.cn/col/col48038/index.html',
        }

    def get_data(self,url):
        response = requests.get(url,headers=self.headers)
        return response.content

    def parse_list_page(self,data):
        with open('js.html','wb') as f:
            f.write(data)
        # 将html转换为element对象
        html = etree.HTML(data)
        # print(html)
        # data1 = urllib.request.urlopen(self.url).read().decode('utf-8', 'ignore')
        # print(data1)
        # 获取详情页面的节点列表
        note_list = html.xpath('//*[@id="thread_list"]/li[@class=" j_thread_list clearfix"]/div/div[2]/div[1]/div[1]/a')

        # n_list =  "<a style=.*?href=(.*?) target=.*?"
        # note_list = re.compile(n_list,re.S).findall(data1)
        print(note_list)
        print(len(note_list))

    def run(self):
        # 构建url
        # 构建请求头
        # 发送请求获取响应(获取列表也的响应)
        data = self.get_data(self.url)
        # print(data)

        # 从响应中抽取详情页面的数据列表
        self.parse_list_page(data)
        # 编辑列表,发起请求(获取详情页面的响应)
        # 从详情页面的响应中抽取列表数据
        # 翻页

if __name__ == '__main__':
    jsd = jsds()
    jsd.run()























