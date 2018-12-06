#
from urllib.parse import urljoin

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
    name = 'eet'
    allowed_domains = ['eet-china.com']
    start_urls = ['https://www.eet-china.com/']

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
            'Ele_Industry.pipelines.ElePipeline14': 300,
        },
        DOWNLOAD_DELAY=0,
        ROBOTSTXT_OBEY=False,

        # 除非真的需要否则就禁止cookies
        # COOKIES_ENABLED=False
        LOG_FILE="LOG_INFO/eet.log",
        # 禁止重试遇到错误不在retry
        # RETRY_ENABLED=False
        LOG_LEVEL="INFO",
        # AJAXCRAWL_ENABLED=True
        DEPTH_LIMIT= 2
        # allow_redirects=False
    )
    rules = (
        Rule(LinkExtractor(allow=r'/tag/.*/'), follow=True),
        Rule(LinkExtractor(allow=r'/news/\d+.html'),callback='parse_item2',follow=True),
    )

    def parse_item2(self,response):

        content = response.xpath('//div[@class="art-con article_body"]')
        if content!= []:
            content = content.extract_first()
            title = response.xpath('//h1')
            if title!= []:
                item = EleIndustryItem()
                title = title.xpath('string(.)').extract_first().strip()

                node1 = response.xpath('//div[@class="detailwarn"]')
                if node1!= []:
                    data = node1.xpath('string(.)').extract_first()
                    time1 = re.findall(r'\d+-\d+-\d+',data)
                    author = re.findall(r'作者：(.*)',data)
                    if time1 != []:
                        time1 = time1[0]+' ' + Get_Time()
                        author1 = ''
                        if author != []:
                            author1 = author[0].strip()
                        abstract = response.xpath('//span[@class="art-lead-text"]/text()').extract_first()
                        Keywords = response.xpath('//div[@class="art-relative-tags"]/a/text()').extract()
                        Keywords = ','.join(Keywords)
                        item['News_Title'] = title
                        item['News_Dt'] = time1
                        item['Author'] = author1
                        item['Keywords'] = Keywords
                        item['Abstract'] = abstract
                        str_time = '<div class="explain"><span>' + item['Author'] + '</span><time>' + str(
                            item['News_Dt'].split(' ')[0]) + '</time></div>'
                        content1 = '<h1>' + item[
                            'News_Title'] + '</h1>' + str_time + "<div class='content'>" + content + "</div>"
                        data = change_content(content1, 'https://www.eet-china.com')
                        item['Content'] = data[0]
                        img_url2 = ''
                        img = response.xpath('//div[@class="cover-img"]/@style').extract_first()
                        if img is not None:              
                            img = img.replace('(','').replace(')','')
                            img_url = re.search(r'url(.*)',img)
                            if img_url:
                                img_url1 = img_url.group(1)
                                img_url2 = urljoin('https://www.eet-china.com',img_url1)
                        img_list = data[1]
                        if img_list == []:
                            if img_url2 != '':
                                img_list.append(img_url2)
                        get_pic(item, img_list)
                        item['Update_Tm'] = get_time_stamp()
                        item['URL'] = response.url
                        item['Web_Id'] = '5-38'
                        #print(item)
                        yield item
