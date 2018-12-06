import scrapy
import time
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import logging
import requests
import json
# from tools.time import Get_Time
# from items import EleIndustryItem
from lxml import etree
# from tools.Get_img import get_pic
# from tools.timestamp import get_time_stamp
import re

# from tools.get_content import change_content
from items import EleIndustryItem

from tools.Get_img import get_pic
from tools.get_content import change_content
from tools.timestamp import get_time_stamp

from tools.time import Get_Time


class ElecfansSpider(CrawlSpider):
    name = 'cena'
    allowed_domains = ['cena.com.cn']
    start_urls = ['http://www.cena.com.cn/index_1.html']

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
            'Ele_Industry.pipelines.ElePipeline10': 300,
        },
        DOWNLOAD_DELAY=0,
        ROBOTSTXT_OBEY=False,

        # 除非真的需要否则就禁止cookies
        # COOKIES_ENABLED=False
        LOG_FILE="LOG_INFO/cena.log",
        # 禁止重试遇到错误不在retry
        # RETRY_ENABLED=False
        LOG_LEVEL="INFO",
        # AJAXCRAWL_ENABLED=True
        DEPTH_LIMIT=0
        # allow_redirects=False
    )
    # num = time.strftime('%Y%m%d', time.localtime(time.time()))
    rules = (
        Rule(LinkExtractor(allow=r'/index.html'),follow=True),
        #Rule(LinkExtractor(allow=r'/index_\d+.html'),  follow=True),

        Rule(LinkExtractor(allow=r'/index_1.html'),callback='parse_item2',follow=True),
        Rule(LinkExtractor(allow=r'/index_2.html'), callback='parse_item2', follow=True),
        Rule(LinkExtractor(allow=r'/.*?/\d+/\d+.html'), callback='parse_item1', follow=True),

    )

    def parse_item1(self,response):
        # print(response.url)
        # print(response.url)
        content = response.xpath('//*[@id="art_body"]')
        if content!= []:
            content = content.extract_first()
            title = response.xpath('//h1')
            if title!= []:
                item = EleIndustryItem()
                title = title.xpath('string(.)').extract_first().strip()
                time1 = response.xpath('//span[@class="time"]')
                if time1!= []:
                    time1 = re.findall(r'\d+-\d+-\d+',time1.extract_first())
                    if time1 != []:
                        time1 = time1[0]+' ' + Get_Time()
                        author = response.xpath('//span[@class="zuozhe"]').xpath('string(.)').extract_first()
                        if author == '作者：':
                            author = ''
                        Keywords = response.xpath('//span[@class="mbx"]/text()').extract_first()
                        item['News_Title'] = title
                        item['News_Dt'] = time1
                        item['Author'] = author
                        item['Keywords'] = Keywords
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
                        item['Web_Id'] = '5-34'
                        #print(item)
                        yield item


