

import redis
import threadpool

from tianyanchaspider.get_tianyancha import Tianyancah

# i = 0

r = redis.Redis(host='localhost',port=6379, db=0)
# tr = 0
# count = 0
def get_corp(my_task):
    while True:
        company_name = r.blpop("tyc_names", 0)[1].decode("utf-8")
        # print(company_name)
        company_name = company_name.replace(r"\xa0", "")
        try:
            # print("天眼查")
            # print(company_name)
            # re = To_sql()
            ti = Tianyancah(company_name)
            item = ti.get_list()
            print(item.name)
            print(item.product)
            print(item.compat)
            print(item.keyword)
            print(item.faren)
            print(item.phone)
            print(item.email)
            print(item.guanwang)
            print(item.dizhi)
            print(item.gongshangzhuce)
            print(item.zuzhijigoudaima)
            print(item.tongyixinyongdaima)
            print(item.comp_type)
            print(item.hangye)
            print(item.jyfw)
            print(item.zhucedizhi)
            print(item.dengjijiguan)
            print(item.yingwenming)
            print(item.jianjie)
            # re.process_item(item)
            # time.sleep(5)
        except Exception as e:
            print(e)
            r.rpush("tyc_names", company_name)
            # i = input('11111')


# if __name__ == "__main__":
#     try:
#         gevent.monkey.patch_socket()
#         pool = gevent.pool.Pool()
#         for i in range(50):
#             pool.add(gevent.spawn(get_corp))
#         pool.join()
#     except Exception as e:
#         print(e)

if __name__ == "__main__":
    my_task = [i for i in range(1,40)]
    try:
        pool = threadpool.ThreadPool(40)
        mycorp = threadpool.makeRequests(get_corp,my_task)
        [pool.putRequest(req) for req in mycorp]
        pool.wait()
    except Exception as e:
        pass



