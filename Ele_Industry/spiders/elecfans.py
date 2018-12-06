# -*- coding: utf-8 -*-
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
    name = 'elecfans'
    allowed_domains = ['elecfans.com']
    start_urls = ['http://www.elecfans.com/']
    #start_urls = ['http://www.elecfans.com/d/','http://www.elecfans.com/','http://www.elecfans.com/news/hangye/','http://www.elecfans.com/news/report/','http://www.elecfans.com/technical/all/','http://www.elecfans.com/application/','http://www.elecfans.com/news/hangye/','http://www.elecfans.com/technical/','http://www.elecfans.com/xinkeji/']

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

            'Ele_Industry.pipelines.ElePipeline': 300,

        },
        DOWNLOAD_DELAY=0,
        ROBOTSTXT_OBEY=False,
        CONCURRENT_REQUESTS_PER_DOMAIN = 10, 
        # 除非真的需要否则就禁止cookies
        # COOKIES_ENABLED=False
        LOG_FILE="LOG_INFO/elecfans.log",
        # 禁止重试遇到错误不在retry
        # RETRY_ENABLED=False
        LOG_LEVEL="INFO",
        # AJAXCRAWL_ENABLED=True
        DEPTH_LIMIT=1
        # allow_redirects=False
    )

    rules = (
        Rule(LinkExtractor(allow=r'/d/\d+.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/.*/\d+/\d+/\d+/\d+.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/.*/\d+/\d+/\d+.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'http://bbs.elecfans.com/.*_\d+_\d+_\d+.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/.*/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        content = response.xpath('//div[@class="simditor-body clearfix"]')
        if content == []:
            content1 = response.xpath('//div[@class="pct"]')
            if content1 != []:
                content1 = content1.extract_first()
                time1 = response.xpath('//div[@class="bar_tip float_l"]/em/span/@title')
                if time1 == []:
                    time1 = response.xpath('//div[@class="bar_tip float_l"]/em/text()')
                if time1 != []:
                    time1 = time1.extract_first()
                    time1 = re.findall(r'(\d+-\d+-\d+)',time1)
                    if time1!=[]:
                        title = response.xpath('//*[@id="thread_subject"]/text()')
                        if title != []:
                            item = EleIndustryItem()
                            title = title.extract_first()
                            item['News_Title'] = title
                            time1 = time1[0]
                            time1 = time1 + ' ' + Get_Time()
                            item['News_Dt'] = time1
                            author = response.xpath('//div[@class="bar_tip float_l"]/div/span/a/span/text()')
                            author1 = ''
                            if author != []:
                                author1 = author.extract_first()
                            item['Author'] = author1
                            str_time = '<div class="explain"><span>' + item['Author'] + '</span><time>' +  str(item['News_Dt'].split(' ')[0]) + '</time></div>'
                            content1 = '<h1>' + item[
                                'News_Title'] + '</h1>' + str_time + "<div class='content'>" + content1 + "</div>"
                            data= change_content(content1,self.start_urls[0])
                            item['Content'] = data[0]
                            # content2 = etree.HTML(item['Content'])
                            img_list = data[1]
                            get_pic(item, img_list)
                            item['Update_Tm'] = get_time_stamp()
                            item['Abstract'] = ''
                            item['Keywords'] = ''
                            item['URL'] = response.url
                            item['Web_Id'] = '5-24'
                            #print(item)
                            yield item


            if content1 == []:
                content2 = response.xpath('//div[@class="article-content"]')
                content3 = response.xpath('//div[@class="author_des"]')
                if content2!=[]:
                    content2 = content2.extract_first()
                    title = response.xpath('//h1/text()')
                    if title != []:
                        title = title.extract_first()
                        time1 = response.xpath('//div[@class="fl"]/em[3]/text()')
                        if time1!= []:
                            item = EleIndustryItem()
                            time1 = time1.extract_first().replace('年','-').replace('月','-').replace('日','')
                            time1 = time1.strip().split(' ')[0]
                            time1 = time1+' '+ Get_Time()
                            author = response.xpath('//div[@class="fl"]/em[1]/text()')
                            author1 = ''
                            if author != []:
                                author1 = author.extract_first()
                            tag = response.xpath('//div[@class="tag"]//span').xpath('string(.)').extract()
                            tags = ','.join(tag)
                            item['News_Title'] = title
                            item['Author'] = author1
                            item['News_Dt'] = time1
                            item['Keywords'] = tags

                            str_time = '<div class="explain"><span>' + item['Author'] + '</span><time>' + \
                                       item['News_Dt'].split(' ')[0] + '</time></div>'
                            content_1 = '<h1>' + item[
                                'News_Title'] + '</h1>' + str_time + "<div class='content'>" + content2 + "</div>"
                            data= change_content(content_1,self.start_urls[0])
                            item['Content'] = data[0]
                            # content2 = etree.HTML(item['Content'])
                            img_list = data[1]
                            get_pic(item, img_list)
                            item['Update_Tm'] = get_time_stamp()
                            item['Abstract'] = ''
                            item['URL'] = response.url
                            item['Web_Id'] = '5-24'
                            #print(item)
                            yield item


                if content3 != []:
                    content3 = content3.extract_first()
                    title = response.xpath('//h1/text()')
                    if title != []:
                        title = title.extract_first()
                        span_node = response.xpath('//span[@class="float_left font-small color_gray"]').xpath('string(.)').extract_first()
                        span_text = span_node.split(' ')
                        if len(span_text) == 3:
                            item = EleIndustryItem()
                            author = span_text[0].replace('\r','').replace('\n','').replace('\t','').replace('发表于','')
                            time1 = span_text[1]+' '+ Get_Time()
                            tag = response.xpath('//ul[@class="article_tags clearfix"]/li/span').xpath('string(.)').extract()
                            tags = ','.join(tag)
                            item['News_Title'] = title
                            item['Author'] = author
                            item['News_Dt'] = time1
                            item['Keywords'] = tags
                            str_time = '<div class="explain"><span>' + item['Author'] + '</span><time>' + \
                                       item['News_Dt'].split(' ')[0] + '</time></div>'
                            content_1 = '<h1>' + item[
                                'News_Title'] + '</h1>' + str_time + "<div class='content'>" + content3 + "</div>"
                            data= change_content(content_1,self.start_urls[0])
                            item['Content'] = data[0]
                            # content2 = etree.HTML(item['Content'])
                            img_list = data[1]
                            get_pic(item, img_list)
                            item['Update_Tm'] = get_time_stamp()
                            item['Abstract'] = ''
                            item['URL'] = response.url
                            item['Web_Id'] = '5-24'
                            #print(item)
                            yield item




        if content != []:
            content = content.extract_first()
            title = response.xpath('//h1/text()')
            if title != []:
                title = title.extract_first()
                time1 = response.xpath('//section//span[@class="time"]/text()')
                if time1 != []:
                    item = EleIndustryItem()
                    item['News_Title'] = title
                    time1 = time1.extract_first().replace('年','-').replace('月','-').replace('日','')
                    time1 = time1.strip().split(' ')[0]
                    time1 = time1+' '+ Get_Time()
                    item['News_Dt'] = time1
                    author2 = response.xpath('//div[@class="article-info art-share-layout m-share-layout clearfix"]/a').xpath('string(.)').extract()
                    author = '电子发烧友网'
                    if author2!= []:
                        author = author2[0]
                        if author == '':
                            author = '电子发烧友网'
                    if author2 == ['']:
                        uid = response.xpath('//input[@id="webMID"]/@value')
                        if uid != []:
                            uid = uid.extract_first()
                            url = 'http://www.elecfans.com/webapi/member/getUserInfoNew/uid/{}'.format(str(uid))
                            data = requests.get(url).text
                            try:
                                data = json.loads(data)['data']['writer_uname']
                                author = data
                            except Exception as E:
                                pass
                    item['Author'] = author
                    tags = response.xpath('//ul[@class="hot-main clearfix"]/li/text()').extract()
                    tag = ''
                    if tags != []:
                        tag = ','.join(tags).replace('\n','').replace('\r','').replace(' ','').replace(',,',',').strip(',')
                    item['Keywords'] = tag
                    str_time = '<div class="explain"><span>' + item['Author'] + '</span><time>' + \
                               item['News_Dt'].split(' ')[0] + '</time></div>'
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
                    item['Web_Id'] = '5-24'
                    #print(item)
                    yield item



