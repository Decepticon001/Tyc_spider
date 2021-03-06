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


class ElecfansSpider(CrawlSpider):
    name = 'cntronics'
    allowed_domains = ['cntronics.com']
    start_urls = ['http://www.cntronics.com/']
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

            'Ele_Industry.pipelines.ElePipeline2': 300,

        },
        DOWNLOAD_DELAY=0,
        ROBOTSTXT_OBEY=False,

        # 除非真的需要否则就禁止cookies
        # COOKIES_ENABLED=False
        LOG_FILE="LOG_INFO/cntronics.log",
        # 禁止重试遇到错误不在retry
        # RETRY_ENABLED=False
        LOG_LEVEL="INFO",
        # AJAXCRAWL_ENABLED=True
        DEPTH_LIMIT=3
        # allow_redirects=False
    )

    rules = (
        Rule(LinkExtractor(allow=r'/.*/\d+'), callback='parse_item1', follow=True),
        Rule(LinkExtractor(allow=r'/.*/\d+/\d+'), callback='parse_item1', follow=True),
        Rule(LinkExtractor(allow=r'/art/artinfo/id/\d+'), callback='parse_item1', follow=True),
        Rule(LinkExtractor(allow=r'/.*-art/\d+'), callback='parse_item1',follow=True),
    )




    def parse_item1(self,response):
        content= response.xpath('//div[@class="content"]')
        if content != []:
            item = EleIndustryItem()
            content = content.extract_first()
            title = response.xpath('//h2/text()')
            if title!=[]:
                title = title.extract_first()
                time1 = response.xpath('//div[@class="title-box"]/p/span[1]/text()')
                if time1!=[]:
                    time1 = time1.extract_first().split('：')[1] + ' '+  Get_Time()
                    author = response.xpath('//div[@class="title-box"]/p/span[2]/text()')
                    author1 = ''
                    if author != []:
                        author1 = author.extract_first().split('：')[1]
                        if author1.endswith('.com'):
                            author1 = ''
                    item['News_Title'] = title
                    item['News_Dt'] = time1
                    item['Author'] = author1
                    item['Keywords'] = ''
                    str_time = '<div class="explain"><span>' + item['Author'] + '</span><time>' + str(
                        item['News_Dt'].split(' ')[0]) + '</time></div>'
                    content1 = '<h1>' + item[
                        'News_Title'] + '</h1>' + str_time + "<div class='content'>" + content + "</div>"
                    data= change_content(content1,self.start_urls[0])
                    item['Content'] = data[0]
                    # content2 = etree.HTML(item['Content'])
                    img_list = data[1]
                    get_pic(item, img_list)
                    item['Update_Tm'] = get_time_stamp()
                    item['Abstract'] = ''
                    item['URL'] = response.url
                    item['Web_Id'] = '5-26'
                    yield item

