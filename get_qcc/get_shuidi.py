# -*- coding: utf-8 -*-
import redis
import requests
import random

import threadpool
from lxml import etree
import json
r = redis.Redis(host='localhost',port=6379, db=0)
# def get_pro():
#     with open('../file/ips.txt', 'r', encoding='utf-8') as f:
#         list1 = f.readlines()
#     ip = random.choice(list1).strip()
#     # ip = '27.22.79.72:27807'
#     # print(ip)
#     proxy = {
#         'http': '%s' % ip,
#         'https':'%s' % ip,
#     }
#     return proxy

#目标网址
targetUrl = "https://www.taobao.com/help/getip.php"

#http代理接入服务器地址端口
proxyHost = "http-proxy-sg1.dobel.cn"
proxyPort = "9180"

#账号密码
proxyUser = "HUIHANHTTTEST1"
proxyPass = "LDJUC95z"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
	"host" : proxyHost,
	"port" : proxyPort,
	"user" : proxyUser,
	"pass" : proxyPass,
}

proxies = {
	"http"  : proxyMeta,
	"https" : proxyMeta,
}


def get_pro():
    with open('../file/ips.txt', 'r', encoding='utf-8') as f:
        list1 = f.readlines()
    ip = random.choice(list1).strip()
    # ip = '221.230.216.29:26027'
    # print(ip)
    proxy = {
        'http': '%s' % ip,
        'https': '%s' % ip
    }
    return proxy

def get_jyfw(company_name):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'shuidi.cn',
        'Referer': 'http://shuidi.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }

    cookies = {'guid': '7dff802e200b11d8346c66f9e5eeb489', ' pa_guid': 'ef2ecb8a2da40ce141e4534df541f86e', ' UM_distinctid': '166566551e18a8-0c97db32005c17-346a7809-1aeaa0-166566551e2322', ' Hm_lvt_4cb0385b9ad8022cb597e5015cb7a9e8': '1539047773', ' CNZZDATA1256666129': '1754679937-1539045044-http%253A%252F%252Fshuidi.cn%252F%7C1539066644', ' Hm_lpvt_4cb0385b9ad8022cb597e5015cb7a9e8': '1539071086'}

    session = requests.session()
    session.headers = headers
    requests.utils.add_dict_to_cookiejar(session.cookies, cookies)
    # proxies = get_pro()
    res = requests.get("http://shuidi.cn/b-search?key=%s"%(company_name),proxies=proxies,timeout=10).text
    print(res)
    return
    # result = session.get(targetUrl, proxies=proxies)
    # print(result.text)
    selector = etree.HTML(res)
    u = selector.xpath("/html/body/div[3]/div[1]/div[5]/div/div[2]/div[3]/a/@href")
    # print(u)
    url = "http://shuidi.cn"+u[0]
    response = session.get(url,proxies=proxies,timeout=10).text
    selector = etree.HTML(response)
    jyfw = selector.xpath('//*[@id="m111"]/div[@class="detail-info"]/table[@class="table1"]/tr[7]/td[2]')[0]
    jyfw = jyfw.xpath('string(.)')
    ul = '%s?action=page_changes&npage=1'%url
    biangengjilu = session.get(ul,proxies=proxies,timeout=10).text
    bg = json.loads(biangengjilu)
    bgjl = bg["data"]
    for i in range(2,int(bg["spage"])+1):
        ul = '%s?action=page_changes&npage=%s'%(url,str(i))
        biangengjilu = session.get(ul,proxies=proxies,timeout=10).text
        bg = json.loads(biangengjilu)
        bgjl = bgjl+bg["data"]
    da = {
        'jyfw':jyfw,
        'change':bgjl
    }
    data = json.dumps(da,ensure_ascii=False)
    return data

def get_shui(task):
    i = 0
    k = 0
    while True:
        try:
            company_name = r.blpop('test_tyc_names', 0)[1].decode("utf-8")
            company_name = company_name.replace(r"\xa0", "")
            if company_name.startswith("#") or company_name.startswith("$"):
                company_name = company_name[1:]
            data = get_jyfw(company_name)
            # print(company_name)
            k = k+1
            print(data)
            print(k)
        except Exception as e:
            print(e)
            r.rpush('test_tyc_names',company_name)
# get_shui()

if __name__ == "__main__":
    my_task = [i for i in range(0,10)]
    try:
        pool = threadpool.ThreadPool(10)
        mycorp = threadpool.makeRequests(get_shui,my_task)
        [pool.putRequest(req) for req in mycorp]
        pool.wait()
    except KeyboardInterrupt as e1:
        pass
    except Exception as e:
        pass
    except:
        pass
