import json
import re

# from tools.get_content import change_content
from urllib.parse import urljoin

from lxml import etree

import scrapy
from items import EleIndustryItem
from scrapy.spiders import CrawlSpider, Spider

from tools.Get_img import get_pic
from tools.get_content import change_content
from tools.timestamp import get_time_stamp

from tools.time import Get_Time
import re
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import requests

from tools.time import get_data_time


class ElecfansSpider(Spider):
    name = 'heqw'
    # 1630
    allowed_domains = ['hqew.com']
    # start_urls = ['http://www.ofweek.com/CATList-8100-CHANGYIEXINWE-{}html'.format(i) for i in range(1,37343)]

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
            'Ele_Industry.middlewares.MyproxiesSpiderMiddleware': 100,
           
        },
        ITEM_PIPELINES={
            'Ele_Industry.pipelines.ElePipeline12': 400,
        },
        DOWNLOAD_DELAY=0,
        ROBOTSTXT_OBEY=False,



        # 除非真的需要否则就禁止cookies
        # COOKIES_ENABLED=False
        LOG_FILE="LOG_INFO/hewq.log",
        # 禁止重试遇到错误不在retry
        # RETRY_ENABLED=False
        LOG_LEVEL="INFO",
        # AJAXCRAWL_ENABLED=True
        # DEPTH_LIMIT=
        # allow_redirects=False
        # REDIRECT_ENABLED=False
    )

    def start_requests(self):
        url = 'http://news.hqew.com/home/load'
        url2 = 'http://news.hqew.com/'
        yield scrapy.Request(url2,callback=self.parse_page1)

        # FormRequest 是Scrapy发送POST请求的方法6353
        for num in range(2,5):
            yield scrapy.FormRequest(
                url=url,
                formdata={"PageIndex": str(num), "OrderBy": '',"Date": get_data_time()},
                callback=self.parse_page
            )



    def parse_page(self,response):
        data = response.body_as_unicode()
        if data != []:
            items = []
            data = json.loads(data)
            for i in data:
                item = EleIndustryItem()
                Abstract = i['Content']
                ImageUrl = i['ImageUrl']
                title = i['Subject']
                id  = i['Itemid']
                TimeDes = i['TimeDes']
                TagList = i['TagList']
                url1 = urljoin('https://m.hqew.com', '/news/' + str(id))
                #tags = [j['TagName'] for j in TagList]
                #tags = [ j['TagName'].strip() for j in TagList if j['TagName'] is not None]
                #keywords = ','.join(tags)
               	tags = []
                for i in TagList:
                    if i['TagName'] is not None:
                        tags.append(i['TagName'])
                keywords = ','.join(tags)
                time1 = re.findall(r'\d+-\d+-\d+',TimeDes)[0] + ' ' + Get_Time()
                item['Abstract'] = Abstract
                item['News_Title'] = title
                item['News_Dt'] = time1
                item['URL'] = url1
                item['Keywords'] = keywords
                item['Image_URL'] = ImageUrl
                items.append(item)
            for item in items:
                yield scrapy.Request(item['URL'],callback=self.parse_detail,meta={'meta_1':item})


    def parse_page1(self,response):
        nodes = response.xpath('//ul[@class="news-items"]/li')
        items = []
        for node in nodes:
            title = node.xpath('.//h3/a/text()').extract_first()
            url = node.xpath('.//h3/a/@href').extract_first()
            num = re.findall(r'\d+',url)
            url1 = urljoin('https://m.hqew.com','/news/'+str(num[0]))
            Abstract = node.xpath('.//p/text()').extract_first().strip()
            tags = node.xpath('.//div[@class="news-item-tag"]/a/text()').extract()
            keywords = ','.join(tags)
            time1 = node.xpath('.//div[@class="news-item-time"]/text()').extract_first()
            time1 = re.findall(r'\d+-\d+-\d+', time1)[0] + ' ' + Get_Time()
            ImageUrl = node.xpath('.//img/@src').extract_first()
            item = EleIndustryItem()
            item['Abstract'] = Abstract
            item['News_Title'] = title
            item['News_Dt'] = time1
            item['URL'] = url1
            item['Keywords'] = keywords
            item['Image_URL'] = ImageUrl
            items.append(item)
        for item in items:
            yield scrapy.Request(item['URL'],callback=self.parse_detail,meta={'meta_1':item})


    def parse_detail(self,response):
        item = response.meta['meta_1']
        content = response.xpath('//*[@id="newsInfo"]')
        if content != []:
            content = content.extract_first()
            item['Author'] = '华强资讯'
            item['URL'] = response.url
            str_time = '<div class="explain"><span>' + item['Author'] + '</span><time>' + str(
                item['News_Dt'].split(' ')[0]) + '</time></div>'
            content1 = '<h1>' + item[
                'News_Title'] + '</h1>' + str_time + "<div class='content'>" + content + "</div>"
            data = change_content(content1,'http://news.hqew.com')
            item['Content'] = data[0]
            if data[1]!=[]:
                data[1].pop()
            if data[1] == []:
                data[1].append(item['Image_URL'])
            img_list = data[1]
            get_pic(item, img_list)
            item['Update_Tm'] = get_time_stamp()
            item['Web_Id'] = '5-36'
            #print(item)
            yield item


