import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import logging
import requests
import json
from tools.time import Get_Time
from items import EleIndustryItem
from lxml import etree
from tools.Get_img import get_pic
from tools.timestamp import get_time_stamp
import re

from tools.get_content import change_content
import re
import re
class ElecfansSpider(CrawlSpider):
    name = 'ET'
    allowed_domains = ['eetop.cn']
    start_urls = ['http://www.eetop.cn/blog/html/45/category-catid-145.html']
    # start_urls = ['http://spaces.eepw.com.cn/']
    # start_urls = ['http://www.ic112.com/List/index/cid/1.html','http://www.ic112.com/List/index/cid/2.html','http://www.ic112.com/List/index/cid/3.html','http://www.ic112.com/List/index/cid/4.html','http://www.ic112.com/List/index/cid/5.html','http://www.ic112.com/List/index/cid/6.html','http://www.ic112.com/List/index/cid/7.html','http://www.ic112.com/List/index/cid/8.html','http://www.ic112.com/List/index/cid/9.html']

    custom_settings = dict(
        # JOBDIR =  'job_info/001',
        # CONCURRENT_REQUESTS=100,
        DEFAULT_REQUEST_HEADERS={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        },
        DOWNLOADER_MIDDLEWARES={
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'Ele_Industry.middlewares.UserAgentMiddleware': 300,
        },
        ITEM_PIPELINES={

            'Ele_Industry.pipelines.ElePipeline9': 300,

        },
        DOWNLOAD_DELAY=0,
        ROBOTSTXT_OBEY=False,

        # 除非真的需要否则就禁止cookies
        # COOKIES_ENABLED=False
        LOG_FILE="LOG_INFO/ET.log",
        # 禁止重试遇到错误不在retry
        # RETRY_ENABLED=False
        LOG_LEVEL="INFO",
        # AJAXCRAWL_ENABLED=True
        DEPTH_LIMIT=2
        # allow_redirects=False
    )

    rules = (
        # Rule(LinkExtractor(allow=r'/blog/html/\d+/category-catid-\d+.html'),follow=True),
        Rule(LinkExtractor(allow=r'page-\d+.html'), follow=True),

        Rule(LinkExtractor(allow=r'/blog/html/\d+/n-\d+.html'), callback='parse_item',follow=True),
    )


    def parse_item(self,response):
        content = response.xpath('//*[@id="articlebody"]')
        if content != []:
            item = EleIndustryItem()
            content = content.extract_first()
            node = re.findall(r'<center>.*?</center>', content, re.S)
            if node != []:
                content = content.replace(node[0],'')
            title = response.xpath('//*[@id="articledetail"]/h1/text()')
            if title != []:
                title = title.extract_first().strip()
                node1 = response.xpath('//*[@id="articledetail"]/p/span[2]/text()')
                if node1 != []:
                    node2 = node1.extract_first().split('\xa0\xa0')
                    time1 = re.findall(r'\d+-\d+-\d+',str(node1.extract_first))
                    if time1 != []:
                        time1 = time1[0]+ ' ' +  Get_Time()
                        author = re.findall(r'作者:(.*)',node2[1])
                        author1 = ''
                        if author != []:
                            if author[0].strip() != 'n':
                                author1 = author[0].strip()
                        node3 = response.xpath('//*[@id="navigation"]/p/a[3]/text()')
                        keywords = node3.extract_first()
                        item['News_Title'] = title
                        item['News_Dt'] = time1
                        item['Author'] = author1
                        item['Keywords'] = keywords
                        str_time = '<div class="explain"><span>' + item['Author'] + '</span><time>' + str(
                            item['News_Dt'].split(' ')[0]) + '</time></div>'
                        content1 = '<h1>' + item[
                            'News_Title'] + '</h1>' + str_time + "<div class='content'>" + content + "</div>"
                        item['Content'] = content1
                        content2 = etree.HTML(item['Content'])
                        img_list = content2.xpath('//img/@src')
                        get_pic(item, img_list)
                        item['Update_Tm'] = get_time_stamp()
                        item['Abstract'] = ''
                        item['URL'] = response.url
                        item['Web_Id'] = '5-33'
                        #print(item)
                        yield item




"""
http://www.eetop.cn/blog/html/74/n-37674.html

http://www.eetop.cn/blog/html/10/n-6496410.html
http://xilinx.eetop.cn/viewnews-2883
http://www.eetop.cn/blog/html/68/n-6826868.html
http://www.eetop.cn/blog/html/47/n-6681447.html
http://www.eetop.cn/blog/html/93/n-5719993.html

"""
