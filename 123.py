import time

import pymysql
import redis

r = redis.Redis(host='localhost',port=6379,db=0)

connect = pymysql.connect(
                # host="47.104.73.227",
                host="192.168.1.42",
                db="headline",
                user="root",
                passwd="royasoft",
                charset='utf8',
                use_unicode=True)
cursor = connect.cursor()


try:
    cursor.execute("select corp_name from el_corp_name limit 1,10000")
    # key = key+10000
    res = cursor.fetchall()
    for i in res:
        # print(str(i)[2:-3])
        d = str(i)[2:-3]
        print(d)
        # with open("names.txt","a+") as f:
        #     f.write("%s\n"%d)
        r.rpush("qcc_names", str(i)[2:-3])
except Exception as e:
    print(e)
