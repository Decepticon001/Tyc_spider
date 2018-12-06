# -*- coding: utf-8 -*-
import json
import random

import redis
import requests
from lxml import etree
from tianyanchaspider.item import Item

r = redis.Redis(host='localhost',port=6379, db=0)
post = 61613
queue_name = "com.huihan.qilian.fixcopeofbusiness"
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




class Qichacha:
    name = ''

    def __init__(self,name):
        self.name = name
        # self.item = Item()
        headers = {
            'Host': 'www.qichacha.com',
            'method': 'GET',
            'scheme': 'https',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'path': '/search?key=%E4%B8%8A%E6%B5%B7%E6%8A%95%E8%B5%84',
            'Connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
            'Cache-Control': 'max-age=0',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.qichacha.com/',
            # 'Referer':'https://www.baidu.com/link?url=WJq9oShh_9QfUFM6F5FwYELTIxrwwiI3Ij8S7vPCNrMd_5M9AxCmeLN7nT5kYPg3ynQNJnWapv5h6j83BR1JF5qUVWrUK8Ub6QnOzFionXa&wd=&eqid=e53f41050000911b000000025bb067c7',
            # 'Cache-Control': 'no-cache',
            'upgrade-insecure-requests': '1'
        }

        cookies ={'acw_tc': '8ccd3b4815365646281052505ea6f79f1fd917b5a815593cd8a3437a39', ' UM_distinctid': '165c2638e0572a-0e0617aef8c12b-1033685c-1aeaa0-165c2638e06e42', ' zg_did': '%7B%22did%22%3A%20%22165c2638ea4af1-062a5e066175e-1033685c-1aeaa0-165c2638ea53a9%22%7D', ' _uab_collina': '153656462962156186441343', ' QCCSESSID': 'gqqepicg7vck76qo7025va6qs1', ' hasShow': '1', ' _umdata': 'A502B1276E6D5FEF382CD5222D0EEA9BBBFD91DE1A3CDEA21BA02DB34377C5B321A62688965FE672CD43AD3E795C914CE8ACA17A71E244374B59E17288A21CF8', ' Hm_lvt_3456bee468c83cc63fb5147f119f1075': '1538287568,1538287582,1538287592,1538287605', ' CNZZDATA1254842228': '56293974-1536561604-https%253A%252F%252Fwww.qichacha.com%252F%7C1538290547', ' zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f': '%7B%22sid%22%3A%201538293164207%2C%22updated%22%3A%201538293166718%2C%22info%22%3A%201538287353795%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22fc81a9275bcfd2edce2b31f2354e585c%22%7D', ' Hm_lpvt_3456bee468c83cc63fb5147f119f1075': '1538293167'}

        # cookies = {}
        self.session = requests.session()
        self.session.headers = headers
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies)


    def get_pro(self):
        with open('file/ips.txt', 'r', encoding='utf-8') as f:
            list1 = f.readlines()
        ip = random.choice(list1).strip()
        # ip = '221.230.216.29:26027'
        # print(ip)
        proxy = {
            'http': '%s' % ip,
            'https': '%s' % ip
        }
        return proxy

    def get_list(self):
        url = "http://www.qichacha.com/search?key=%s"%(self.name)
        # proxies=proxy,
        response = self.session.get(url,timeout=10)
        html = response.text
        # print(html)
        selector = etree.HTML(html)
        gc = selector.xpath('//*[@id="searchlist"]/table/tbody/tr/td/a/@href')
        url ='http://www.qichacha.com' + gc[0]
        jyfw = self.get_info(url)
        return jyfw


    def get_info(self,url):
        item = Item()
        item.name = self.name
        response1 = self.session.get(url,timeout=10)
        # proxies=proxies,
        html = response1.text
        selector1 = etree.HTML(html)
        jyfw = selector1.xpath('//*[@id="Cominfo"]/table[2]/tr[11]/td[2]/text()')[0].strip()

        change = selector1.xpath('//*[@id="Changelist"]/table/tr')
        # changeProject = selector1.xpath('//*[@id="Changelist"]/table/tr/td[3]')[0]
        # changeBe = selector1.xpath('//*[@id="Changelist"]/table/tr/td[4]')[0]
        # changeAf = selector1.xpath('//*[@id="Changelist"]/table/tr/td[5]')[0]
        changeData=[]
        for i in range(1,len(change)):
            change_data = change[i].xpath('string(.)')
            changeTm = change_data.split()[1]
            changeProject = change_data.split()[2]
            changeBe = change_data.split()[3]
            changeAf = change_data.split()[4]
            change_js = {
                'changeTm':changeTm,
                'changeProject':changeProject,
                'changeBe':changeBe,
                'changeAf':changeAf
            }
            change_js = json.dumps(change_js, ensure_ascii=False)
            changeData.append(change_js)
        data = {
            'companyName': self.name,
            'scopeOfBusiness': jyfw,
            'changeData':changeData
        }
        data = json.dumps(data,ensure_ascii=False)
        return data



def get_test(task):
    # conn = stomp.Connection10([('47.105.121.234', post)])

    while True:
        try:
            company_name = r.blpop('qcc_names', 0)[1].decode("utf-8")
            company_name = company_name.replace(r"\xa0", "")
            if company_name.startswith("#") or company_name.startswith("$"):
                company_name = company_name[1:]
            q = Qichacha(company_name)
            data = q.get_list()
            print(data)
            # cursor.execute("insert into company_info (info) values ('%s')"%(data))
            # connect.commit()

            # comp = {
            #     "companyName":company_name,
            #     "scopeOfBusiness":jyfw
            # }
            # data = json.dumps(comp, ensure_ascii=False)
            # conn.start()
            # conn.connect()
            # conn.send(queue_name, data)
        except Exception as e:
            print(e)
            r.rpush('qcc_names', company_name)
            # print("已放回队列")
    # conn.disconnect()
    connect.close()

# if __name__ == '__main__':
#     my_task = [i for i in range(0, 50)]
#     try:
#         pool = threadpool.ThreadPool(50)
#         mycorp = threadpool.makeRequests(get_test, my_task)
#         [pool.putRequest(req) for req in mycorp]
#         pool.wait()
#     except Exception as e:
#         pass


if __name__ == '__main__':
    q = Qichacha("中通快递股份有限公司")
    jyfw = q.get_list()
    print(jyfw)



