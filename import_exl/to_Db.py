# -*- coding = utf-8 -*-
import os

import openpyxl
import pymysql
import redis

r = redis.Redis(host='localhost',port=6379, db=0)
for i in range(0,10000):
    a = r.rpop("tyc_names")
    print(a)