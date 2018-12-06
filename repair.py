
import redis

r = redis.Redis(host='localhost',port=6379,db=0)

with open('/Users/pengzhishen/Downloads/PycharmProjects/get_name_by_city/names.txt',"r") as f:
    a = f.readlines()

for i in a:
    r.rpush("company_name", i.strip())