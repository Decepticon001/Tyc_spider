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

from New_Work.Ele_Industry.Ele_Industry.tools.change_time import GetTime
from New_Work.Ele_Industry.Ele_Industry.tools.change_url import md5_url

class ElecfansSpider(CrawlSpider):
    name = 'AET'
    allowed_domains = ['chinaaet.com']
    start_urls = ['http://www.chinaaet.com/news/']
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
            'Ele_Industry.pipelines.ElePipeline11': 300,
        },
        DOWNLOAD_DELAY=0,
        ROBOTSTXT_OBEY=False,
        # 除非真的需要否则就禁止cookies
        # COOKIES_ENABLED=False
        LOG_FILE="LOG_INFO/AET.log",
        # 禁止重试遇到错误不在retry
        # RETRY_ENABLED=False
        LOG_LEVEL="INFO",
        # AJAXCRAWL_ENABLED=True
        DEPTH_LIMIT=0
        # allow_redirects=False
    )

    rules = (
        Rule(LinkExtractor(allow=r'http://www.chinaaet.com/news/\d+#lastest'),follow=True),
        # Rule(LinkExtractor(allow=r'http://www.chinaaet.com/news/2#lastest'), follow=True),
        Rule(LinkExtractor(allow=r'/article/\d+'), callback='parse_item'),
    )


    def parse_item(self,response):
        content = response.xpath('//div[@class="article-bd"]')
        if content != []:
            item = EleIndustryItem()
            content = content.extract_first()
            title = response.xpath('//h1[@class="title-h1"]/text()')
            if title != []:
                title = title.extract_first().strip()
                time1_node = response.xpath('//div[@class="article-attr"]')
                if time1_node != []:
                    time1 = time1_node.xpath('string(.)').extract_first()
                    time1 = time1.replace('/','-')
                    time1 = GetTime(time1)
                    if time1 is not None:
                        author = ''
                        keywords = response.xpath('//span[@class="article-keywords"]/a/text()').extract()
                        keywords = ','.join(keywords)
                        try:
                            content = change_content(content,'//div[@class="article-bd"]')
                        except Exception as E:
                            logging.error('img有错'+response.url)

                        item['newsTitle'] = title
                        item['newsDt'] = time1
                        item['author'] = author
                        item['keywords'] = keywords
                        item['updateTm'] = get_time_stamp()
                        item['abstract'] = ''
                        item['url'] = response.url
                        item['content'] = content
                        item['aid'] = md5_url(item['url'])
                        item['bid'] = '1'
                        yield item


