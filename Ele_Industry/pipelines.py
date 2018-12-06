# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import logging

import pymysql
import stomp
from bloom_filter import BloomFilter

from Ele_Industry.settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWD, MYSQL_DBNAME, MYSQL_HOST1, MYSQL_USER1, MYSQL_PASSWD1, MYSQL_DBNAME1
import json

class EleIndustryPipeline(object):
    def process_item(self, item, spider):
        return item
class ElePipeline11(object):

    def __init__(self):
        self.bf_urls = BloomFilter(max_elements=10000000, error_rate=0.001, filename="Filter_files/urls_AET_1.bf")
        self.bf_content = BloomFilter(max_elements=10000000, error_rate=0.001, filename="Filter_files/title_AET_1.bf")
        self.bf_urls1 = BloomFilter(max_elements=10000000, error_rate=0.001, filename="Filter_files/urls_AET.bf")
        self.bf_content1 = BloomFilter(max_elements=10000000, error_rate=0.001, filename="Filter_files/title_AET2.bf")


    def save(self,item):
        conn = stomp.Connection10([('47.105.80.251', 61613)])
        queue_name = 'com.huihan.qilian.vnews'
        conn.start()
        conn.connect()
        conn.send(queue_name, item)
        conn.disconnect()
        print('保存了')


    def process_item(self, item, spider):
        sha1 = hashlib.sha1()
        sha1.update(item['newsTitle'].encode())
        hashRs = sha1.hexdigest()
        sha2 = hashlib.sha1()
        sha2.update(item['url'].encode())
        hashRs2 = sha2.hexdigest()
        item = json.dumps(dict(item), ensure_ascii=False)
        self.save(item)






        # if hashRs not in self.bf_content and hashRs2 not in self.bf_urls:






