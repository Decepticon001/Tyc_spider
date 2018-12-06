import re

# from tools.get_content import change_content
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
class ElecfansSpider(Spider):
    name = 'eeworld'
    # 1630
    allowed_domains = ['eeworld.com.cn']
    start_urls = ['http://www.eeworld.com.cn']

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
            
            'Ele_Industry.pipelines.ElePipeline6': 300,
        },
        DOWNLOAD_DELAY=0,
        ROBOTSTXT_OBEY=False,

        # 除非真的需要否则就禁止cookies
        # COOKIES_ENABLED=False
        LOG_FILE="LOG_INFO/eeworld.log",
        # 禁止重试遇到错误不在retry
        # RETRY_ENABLED=False
        LOG_LEVEL="INFO",
        # AJAXCRAWL_ENABLED=True
        # DEPTH_LIMIT=
        # allow_redirects=False
    )


    def parse(self,response):
        nodes = response.xpath('//div[@class="cp2liststy"]')
        items = []
        if nodes != []:
            for node in nodes:
                item = EleIndustryItem()
                title = node.xpath('./h4/a/@title').extract_first()
                url =  node.xpath('./h4/a/@href').extract_first()
                time1 = node.xpath('./em/text()').extract_first()
                time1 = re.findall(r'\d+-\d+-\d+',time1)[0]
                time1 = time1 + ' ' + Get_Time()
                keywords = node.xpath('./span/a').xpath('string(.)').extract()
                # keywords = ','.join(keywords)
                Abstract = node.xpath('./div[2]/p/text()').extract_first()
                item['Abstract'] = Abstract
                item['News_Title'] = title
                item['News_Dt'] = time1
                item['URL'] = url
                items.append(item)

        for item in items:
            yield scrapy.Request(item['URL'],callback=self.parse_detail,meta={'meta_1':item},dont_filter=True)

    def parse_detail(self,response):
        content = response.xpath('//div[@class="newscontxt"]')
        item = response.meta['meta_1']
        if content != []:
            content = content.extract_first()
            keywords = response.xpath('//div[@class="newscontxt"]//h4//a').xpath('string(.)').extract()
            item['Keywords'] = ','.join(keywords)
            author1 = 'EEWORLD'
            author = response.xpath('//*[@id="newsptit"]/div[1]/div/h6/span[2]/text()')
            if author !=[]:
                author = author.extract_first()
                author_1 = author.split(':')
                if len(author_1) < 2:
                    author_1 = author.split('：')
                author = author_1[1]
                if author != ' ':
                    author1 = author
            item['Author'] = author1
            str_time = '<div class="explain"><span>' + item['Author'] + '</span><time>' + str(
                item['News_Dt'].split(' ')[0]) + '</time></div>'
            content1 = '<h1>' + item[
                'News_Title'] + '</h1>' + str_time + "<div class='content'>" + content + "</div>"
            item['Content'] = content1
            content2 = etree.HTML(content1)
            img_list = content2.xpath('//img/@src')
            get_pic(item, img_list)
            item['Update_Tm'] = get_time_stamp()
            item['Web_Id'] = '5-30'
            #print(item)
            yield item


"""
http://www.eeworld.com.cn/my/news_ajax.php?catid=1&page=1629&ch=hp&nocatid=47495%2C47492%2C47491%2C47490%2C47487%2C47486%2C47485%2C47484%2C47483%2C47482%2C47481%2C47478


"""
