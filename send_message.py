# -*- coding: utf-8 -*-
import os
import openpyxl
import pika
import pymysql
import redis


connect = pymysql.connect(
                host="192.168.1.42",
                db="headline",
                user="root",
                passwd="royasoft",
                charset='utf8',
                use_unicode=True)
cursor = connect.cursor()
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue="company_name")
key = 535
cursor.execute("select corp_name from el_corp_name where id>%s and id<%s"%(str(key),str(key+1000)))
res = cursor.fetchall()
for name in res:
    d = str(name)[2:-3]
    # print(d)
    channel.basic_publish(exchange='',
                          routing_key='company_name',
                          body='%s'%d)
    print("[x] Sent '%s'"%d)
connection.close()
connect.close()