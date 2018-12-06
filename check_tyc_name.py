import time

import pymysql
import redis
import csv
#
r = redis.Redis(host='localhost',port=6379, db=0)


connect = pymysql.connect(
                host="47.104.73.227",
                db="headline",
                user="root",
                passwd="royasoft",
                charset='utf8',
                use_unicode=True)
cursor = connect.cursor()
key = 283000
while True:
    try:
        lens = r.llen('tyc_names_all')
        if lens < 10:
            cursor.execute("select Corp_Name from tyc_e_corp_cop limit %s,1000" % (str(key)))
            res = cursor.fetchall()
            key = key+1000
            print(len(res))
            for i in res:
                if i != "None":
                    pass
                    # r.rpush("tyc_names_all", i[0])
                    print(i[0])
        time.sleep(10)
    except KeyboardInterrupt as e:
        print(key)
        break
    except Exception as e1:
        print(key)
        print(e1)
        break
connect.close()