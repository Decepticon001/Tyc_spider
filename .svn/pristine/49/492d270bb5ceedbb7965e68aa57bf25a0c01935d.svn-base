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

class ElecfansSpider(CrawlSpider):
    name = 'ic37'
    allowed_domains = ['ic37.com']
    start_urls = ['http://www.ic37.com/htm_news/default.htm']
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
            # 'scrapy.downloadermiddlewares.retry.RetryMiddleware':None,
            'Ele_Industry.middlewares.UserAgentMiddleware': 300,
            # 'Ele_Industry.middlewares.MyproxiesSpiderMiddleware': 100,
        },
        ITEM_PIPELINES={

            'Ele_Industry.pipelines.ElePipeline13': 300,

        },
        DOWNLOAD_DELAY=0,
        ROBOTSTXT_OBEY=False,
        # RETRY_ENABLED = True,
        # RETRY_TIMES = 3
        # 除非真的需要否则就禁止cookies
        # COOKIES_ENABLED=False
        LOG_FILE="LOG_INFO/ic37.log",
        # 禁止重试遇到错误不在retry
        # RETRY_ENABLED=False
        LOG_LEVEL="INFO",
        # AJAXCRAWL_ENABLED=True
        DEPTH_LIMIT=1
        # allow_redirects=False
    )

    rules = (
        #Rule(LinkExtractor(allow=r'/listpage\d+_\d+.htm'),  follow=True),

        Rule(LinkExtractor(allow=r'\d+-\d+/\d+_\d+.htm'), callback='parse_detail',follow=True),
    )


    def parse_item(self,response):
        pass
        # print(response.url)
        # next_url = response.url
        # if not response.url.endswith('r0'):
        #     next_url = response.url + '/r0'
        # yield scrapy.Request(next_url,callback=self.parse_detail)

    def parse_detail(self,response):
        content = response.xpath('//div[@class="contentlist"]')
        if content != []:
            item = EleIndustryItem()
            content = content.extract_first()
            title = response.xpath('//h1/text()')
            if title != []:
                title = title.extract_first().strip()
                node1= response.xpath('//div[@class="newstitle"]/span/text()')
                if node1 != []:
                    node2  = node1.extract_first()
                    time_1 = re.findall(r'\d+-\d+-\d+',node2)
                    if time_1 != []:
                        time1 = time_1[0] + ' ' +  Get_Time()
                        try:
                            author = node2.split('，')[1].strip()
                        except Exception as E:
                            author = ''
                        node3 = response.xpath('//div[@class="newstitle"]/span/a/text()')
                        keywords = ''
                        if node3 != []:
                            keywords = node3.extract_first()

                        item['News_Title'] = title
                        item['News_Dt'] = time1
                        item['Author'] = author
                        item['Keywords'] = keywords
                        str_time = '<div class="explain"><span>' + item['Author'] + '</span><time>' + str(
                            item['News_Dt'].split(' ')[0]) + '</time></div>'
                        content1 = '<h1>' + item[
                            'News_Title'] + '</h1>' + str_time + "<div class='content'>" + content + "</div>"
                        data = change_content(content1, 'http://www.ic37.com')
                        item['Content'] = data[0]
                        img_list = data[1]
                        get_pic(item, img_list)
                        item['Update_Tm'] = get_time_stamp()
                        item['Abstract'] = ''
                        item['URL'] = response.url
                        item['Web_Id'] = '5-37'
                        #print(item)
                        yield item






        # content = response.xpath('//*[@id="contentDiv"]')
        # if content != []:
        #     content = content.extract_first()
        #     title = response.xpath('//h1/text()')
        #     if title !=[]:
        #         title = title.extract_first()
        #         time1 = response.xpath('//div[@class="authorTimeSource"]/span[2]/text()')
        #         if time1 != []:
        #             item = EleIndustryItem()
        #             time1 = time1.extract_first().split('：')[1]
        #             time1 = time1+ ' ' + Get_Time()
        #             author = response.xpath('//div[@class="authorTimeSource"]/span[3]/text()').extract_first()
        #             author = author.split('：')[1]
        #             tags = response.xpath('//div[@class="keyWord"]//em').xpath('string(.)').extract()
        #             key = ','.join(tags)
        #             item['News_Title'] = title
        #             item['News_Dt'] = time1
        #             item['Author'] = author
        #             item['Keywords'] = key
        #             str_time = '<div class="explain"><span>' + item['Author'] + '</span><time>' + str(
        #                 item['News_Dt'].split(' ')[0]) + '</time></div>'
        #             content1 = '<h1>' + item[
        #                 'News_Title'] + '</h1>' + str_time + "<div class='content'>" + content + "</div>"
        #             data = change_content(content1, self.start_urls[0])
        #             item['Content'] = data[0]
        #             img_list = data[1]
        #             get_pic(item, img_list)
        #             item['Update_Tm'] = get_time_stamp()
        #             item['Abstract'] = ''
        #             item['URL'] = response.url
        #             item['Web_Id'] = '5-27'
        #             yield item
