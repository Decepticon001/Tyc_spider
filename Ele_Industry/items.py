# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EleIndustryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 文章标题
    newsTitle = scrapy.Field()
    # 文章url
    url = scrapy.Field()
    # 新闻日期
    newsDt = scrapy.Field()
    # 摘要
    abstract = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 关键字
    keywords = scrapy.Field()
    # 更新时间
    updateTm = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 图片链接1
    Image_URL1 = scrapy.Field()
    # 图片链接2
    Image_URL2 = scrapy.Field()
    # 图片链接3
    Image_URL3 = scrapy.Field()
    # 图片链接4
    Image_URL4 = scrapy.Field()
    webId = scrapy.Field()
    Image_URL = scrapy.Field()
    aid = scrapy.Field()
    bid = scrapy.Field()

