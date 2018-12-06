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
class ElecfansSpider(Spider):
    name = 'ofweek'
    # 1630
    allowed_domains = ['ofweek.com']
    start_urls = ['http://www.ofweek.com/CATList-8100-CHANGYIEXINWE-{}html'.format(i) for i in range(1,5)]

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
            #'Ele_Industry.middlewares.MyproxiesSpiderMiddleware': 100,
        },
        ITEM_PIPELINES={
            'Ele_Industry.pipelines.ElePipeline8': 300,
        },
        DOWNLOAD_DELAY=2,
        ROBOTSTXT_OBEY=False,

        # 除非真的需要否则就禁止cookies
        # COOKIES_ENABLED=False
        LOG_FILE="LOG_INFO/ofweek.log",
        # 禁止重试遇到错误不在retry
        # RETRY_ENABLED=False
        LOG_LEVEL="INFO",
        # AJAXCRAWL_ENABLED=True
        # DEPTH_LIMIT=
        # allow_redirects=False
    )


    def parse(self,response):
        nodes = response.xpath('//div[@class="con-details"]')
        items = []
        if nodes != []:
            for node in nodes:
                item = EleIndustryItem()
                title = node.xpath('.//h3/a/text()').extract_first()
                url =  node.xpath('.//h3/a/@href').extract_first()
                Abstract = node.xpath('.//p/span/text()').extract_first()
                time1 = node.xpath('.//span[@class="fb-tl"]/text()').extract_first()
                time1 = re.findall(r'\d+-\d+-\d+',time1)[0]
                time1 = time1 + ' ' + Get_Time()
                keywords = node.xpath('//span[@class="fb-tl"]/a/text()').extract_first()
                item['Abstract'] = Abstract
                item['News_Title'] = title
                item['News_Dt'] = time1
                item['URL'] = url
                item['Keywords'] = keywords
                items.append(item)

        for item in items:
            yield scrapy.Request(item['URL'],callback=self.parse_detail,meta={'meta_1':item})

    def parse_detail(self,response):
        item = response.meta['meta_1']
        content = response.xpath('//*[@id="articleC"]')
        if content != []:
            content = content.extract_first()
            next_page = response.xpath('//div[@class="page"]')
            if next_page != []:
                next_url = response.xpath('//*[@id="nextPage"]/a/@href').extract_first()
                url = urljoin(response.url, next_url)
                data = requests.get(url)
                content_1= re.findall(r'<div id="articleC" class="article_con" >(.*?)</div>',data.text,re.S)
                content = content+content_1[0]
            author1 = response.xpath('//*[@id="laiyuan_mp"]/a/span/text()')
            author2 = response.xpath('//*[@id="laiyuan"]/span')
            author = author1.extract_first()
            if author is None:
                author = author2.xpath('string(.)').extract_first()
                author = author.split('：')[1].strip()
            item['Author'] = author
            str_time = '<div class="explain"><span>' + item['Author'] + '</span><time>' + str(
                item['News_Dt'].split(' ')[0]) + '</time></div>'
            content1 = '<h1>' + item[
                'News_Title'] + '</h1>' + str_time + "<div class='content'>" + content + "</div>"
            item['Content'] = content1
            content2 = etree.HTML(content1)
            img_list = content2.xpath('//img/@src')
            get_pic(item, img_list)
            item['Update_Tm'] = get_time_stamp()
            item['Web_Id'] = '5-32'
            yield item


"""
http://www.eeworld.com.cn/my/news_ajax.php?catid=1&page=1629&ch=hp&nocatid=47495%2C47492%2C47491%2C47490%2C47487%2C47486%2C47485%2C47484%2C47483%2C47482%2C47481%2C47478

"""
