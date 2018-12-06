# -*- coding: utf-8 -*-
import datetime
import random
import requests
from lxml import etree
from tianyanchaspider.item import Item
from pandas.core.frame import DataFrame
import json

import base64


class Tianyancah:
    name = ''
    n = 1
    def __init__(self,name):
        self.name = name
        USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]
        headers = {
            'Host': 'www.tianyancha.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'user-agent': '%s'%(random.choice(USER_AGENTS)),
            'Cache-Control': 'max-age=0',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            # 'Referer': 'https://www.tianyancha.com/',
            # 'Referer': 'https://www.baidu.com/link?url=aaadddda',
            'Referer':'https://www.baidu.com/link?url=YLvTSuGhlTTvDeRvaJRxwcaZoZfouCq406ty7U_pGKfk9s9Q3iZlqgRhBnchaodzuBpwSzl47wKgPW1jicIoNa&wd=&eqid=e989465400038d08000000065b8f2dd8',
        }
        # cookies = {'aliyungf_tc': 'AQAAAM1yZAitZwoAmjr2OniKlb7eHVwo', ' csrfToken': '60dvZDJ44s2d3rM5SLztpT7F', ' TYCID': '46fe0b00d5ae11e8acbc453f74b7f19e', ' undefined': '46fe0b00d5ae11e8acbc453f74b7f19e', ' ssuid': '7469344412', ' Hm_lvt_e92c8d65d92d534b0fc290df538b4758': '1540180516', ' _ga': 'GA1.2.1242039210.1540180517', ' _gid': 'GA1.2.439109732.1540180517', ' tyc-user-info': '%257B%2522myQuestionCount%2522%253A%25220%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%252224%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODAxNzc0MTE3MCIsImlhdCI6MTU0MDE4MDUyNiwiZXhwIjoxNTU1NzMyNTI2fQ.yEbOGCpts85583Zhyvsbaq1zYSIiIpn_NvfboQsnzeislxdC59GiNFM-4Ccm1jKg8WHjrA8DKXzXz1TxaPbdfw%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25221%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218017741170%2522%257D', ' auth_token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODAxNzc0MTE3MCIsImlhdCI6MTU0MDE4MDUyNiwiZXhwIjoxNTU1NzMyNTI2fQ.yEbOGCpts85583Zhyvsbaq1zYSIiIpn_NvfboQsnzeislxdC59GiNFM-4Ccm1jKg8WHjrA8DKXzXz1TxaPbdfw', ' _gat_gtag_UA_123487620_1': '1', ' Hm_lpvt_e92c8d65d92d534b0fc290df538b4758': '1540184384'}
        cookies={'TYCID': '6cf27140b4d211e8957513e011ebbde4', 'undefined': '6cf27140b4d211e8957513e011ebbde4', 'ssuid': '3108248350', '_ga': 'GA1.2.1978558396.1536567652', 'jsid': 'SEM-BAIDU-CG-SY-002185', 'aliyungf_tc': 'AQAAAPxWOmX72g4Ao5vaQxuKzd8/SDCv', 'csrfToken': 'LSq0jy0voIgVmiAj1mccYtPe', 'token': 'af2c350f121a4ec4b829ab521311d9ed', '_utm': '16c3be868a2948e1b4a7326606b38460', 'cloud_token': '858e066fce2b47dabf29a090c2229e5a', 'tyc-user-info': '%257B%2522myQuestionCount%2522%253A%25220%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%252228%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODAxNzc0MTE3MCIsImlhdCI6MTU0MDU0NjUwMywiZXhwIjoxNTU2MDk4NTAzfQ.f95wx-kWN03ITddHamHRkV_qt1aJTMfz5VX418OJKMG0VjPPpzO49XhhsYYlfEwvefA9ZzhY04Xk24LJ2J-cvA%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25221%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218017741170%2522%257D', 'auth_token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODAxNzc0MTE3MCIsImlhdCI6MTU0MDU0NjUwMywiZXhwIjoxNTU2MDk4NTAzfQ.f95wx-kWN03ITddHamHRkV_qt1aJTMfz5VX418OJKMG0VjPPpzO49XhhsYYlfEwvefA9ZzhY04Xk24LJ2J-cvA', 'Hm_lvt_e92c8d65d92d534b0fc290df538b4758': '1540434183,1540434999,1540435035,1540563519', '_gid': 'GA1.2.751598387.1540776508', '_gat_gtag_UA_123487620_1': '1', 'Hm_lpvt_e92c8d65d92d534b0fc290df538b4758': '1540776521'}

        # cookies = {'TYCID': '699463d0479211e8a2baf1c59485c035', ' undefined': '699463d0479211e8a2baf1c59485c035',
        #            ' ssuid': '4343645724', ' _ga': 'GA1.2.315444768.1531900251', ' jsid': 'SEM-BAIDU-PP-SY-000257',
        #            ' aliyungf_tc': 'AQAAADQJgGoX9wkAmjr2Om4Xic8BfkMl', ' csrfToken': 'bYVVSjjLwZWHkOl3Gpv_goED',
        #            ' token': 'a0d7a7dfd7c74cf5bfa2418d086be058', ' _utm': 'c23d76f505bf4539a74479a144554719',
        #            ' _gid': 'GA1.2.1190140784.1535936900', ' RTYCID': '3150f1a03a7d4b499215b4f208622c9b',
        #            ' CT_TYCID': 'e8c56c8c30534af3b99da05339a922f9',
        #            ' Hm_lvt_e92c8d65d92d534b0fc290df538b4758': '1535973906,1535974043,1535974098,1535977129',
        #            ' Hm_lpvt_e92c8d65d92d534b0fc290df538b4758': '1535977129',
        #            ' cloud_token': '605f4f923a4b473a8b8b561570bd310f', ' cloud_utm': '69fa7577979d4fa99f6aa73f3afe765d',
        #            ' _gat_gtag_UA_123487620_1': '1'}
        self.session = requests.session()
        self.session.headers = headers
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies)

    def get_pro(self):
        with open('/Users/pengzhishen/Downloads/PycharmProjects/get_corp_info/get_corp_info/proxies.txt', 'r') as f:
            ss = f.read()
        ss = ss.replace("'", "")
        proxies = ss[1:-1].split(',')[0:-1]
        # proxy = "https://" + random.choice(proxies).strip()
        proxy = {
            'http': '%s' %  random.choice(proxies).strip(),
            'https': '%s' %  random.choice(proxies).strip()
        }
        return proxy

    def get_list(self):
        item = Item()
        url = "https://www.tianyancha.com/search?key=%s"%(self.name)
        # proxy = self.get_pro()
        response = self.session.get(url,timeout=5)
        # response = self.session.get(url, timeout=10)
        # ,proxies=proxy
        html = response.text
        # print(html)
        selector = etree.HTML(html)
        flag =  selector.xpath('//div[@class="f24 mb40 mt40 sec-c1 "]/text()')
        # print(flag)
        try:
            if flag[0] == '抱歉，没有找到相关结果！':
                item.name = self.name
                item.product = 'Null'
                item.keyword = 'Null'
                item.compat = 'Null'
                return item
        except:
            pass
        u = selector.xpath('//div[@class="search-item"]/div/div[@class="content"]/div/a/@href')[0]
        # print(u)
        item = self.get_info(u)
        # print(u)
        return item
        # print(u)

    def get_info(self,url):
        item = Item()
        item.name = self.name
        company_id = url[35:]
        response = self.session.get(url,timeout=5)
        # response = self.session.get(url, timeout=10)
        # ,proxies=proxy
        html = response.text
        # print(html)
        item = self.get_other(html,item,company_id)
        selector = etree.HTML(html)
        img_url = selector.xpath('//*[@id="company_web_top"]/div[2]/div[1]/div[1]/div[2]/img/@data-src')[0]
        # logo = requests.get(img_url).content
        # logo = base64.b64encode(logo)
        # print(logo)
        # item.logo = logo
        product = selector.xpath('//div[@id="_container_product"]/table/tbody/tr/td[3]/span/text()')
        if product:
            item.product = str(product)[1:-1].replace("'",'')
        else:
            item.product = ""
        jingpin = selector.xpath('//div[@id="_container_jingpin"]/div/table/tbody/tr/td[2]/table/tr/td[2]/a/text()')
        if jingpin:
            item.compat = str(jingpin)[1:-1].replace("'",'')
        else:
            item.compat = ""
        u = selector.xpath('//div[@class="item"]/a/@href')
        if u:
            u = u[0]
        else:
            item.keyword = ""
            return item
        response = self.session.get(u,timeout=5)
        # response = self.session.get(u, timeout=10)
        # ,proxies=proxy
        html = response.text
        selector = etree.HTML(html)
        keyword = selector.xpath("//div[@class='content']/div[3]/a/text()")
        # print(keyword)
        if keyword:
            item.keyword = str(keyword)[1:-1].replace("'",'')
        else:
            item.keyword = ""
        return item


    def get_other(self,html,item,company_id):
        selector = etree.HTML(html)
        faren = selector.xpath('//*[@id="_container_baseInfo"]/table[1]/tbody/tr[1]/td[1]/div/div[1]/div[2]/div[1]/a/text()')
        phone = selector.xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[5]/div[1]/div[1]/span[2]/text()')
        email = selector.xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[5]/div[1]/div[2]/span[2]/text()')
        guanwang = selector.xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[5]/div[2]/div[1]/a/text()')
        dizhi = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[8]/td[2]/text()')
        gongshangzhuce = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[2]/text()')
        zuzhijigoudaima = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[1]/td[4]/text()')
        tongyixinyongdaima = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[2]/text()')
        comp_type = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[2]/td[4]/text()')
        hangye = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[4]/text()')
        jyfw =selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[9]/td[2]/span/span/span/text()')
        zhucedizhi = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[8]/td[2]/text()')
        dengjijiguan = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[6]/td[4]/text()')
        yingwenming = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[7]/td[4]/text()')
        jianjie = selector.xpath('//script[@id="company_base_info_detail"]/text()')
        item.jianjie = ""
        product_des = selector.xpath("//div[@id='_container_desc']/text()")
        regtm = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[4]/td[2]/span/text()')
        nashuirenshibiehao = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[3]/td[2]/text()')
        hezhunriqi = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[4]/td[4]/text/text()')
        zhuceziben = selector.xpath('//*[@id="_container_baseInfo"]/table[1]/tbody/tr[1]/td[2]/div[2]/text/text()')
        jystatus = selector.xpath('//*[@id="_container_baseInfo"]/table[1]/tbody/tr[3]/td/div[2]/text()')
        renyuanguimo = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[5]/td[4]/text()')
        nashuirenzizhi = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[5]/td[2]/text()')
        shijiaoziben = selector.xpath('//*[@id="_container_baseInfo"]/table[2]/tbody/tr[7]/td[2]/text()')
        item.renyuanguimo = str(renyuanguimo)[2:-2]
        item.nashuirenzizhi = str(nashuirenzizhi)[2:-2]
        item.shijiaoziben = str(shijiaoziben)[2:-2]
        main_per_data = DataFrame()
        try:
            main_per_name = selector.xpath('//*[@id="_container_staff"]/div/table/tbody/tr/td[2]/div/a[1]/text()')
            ma = selector.xpath('//*[@id="_container_staff"]/div/table/tbody/tr/td[3]')
            main_per_posit = []
            page = selector.xpath('//*[@id="_container_staff"]/div[@class="company_pager"]')
            pageNum = ''
            if page:
                pageNum = '1'
            for m in ma:
                main_per_posit.append(m.xpath('string(.)').strip())
            main_per = {
                'main_per_name': main_per_name,
                'main_per_posit': main_per_posit,
                'pageNum':pageNum
            }
            main_per_data = DataFrame(main_per)
        except:
            pass
        item.main_per_data = main_per_data

        share_data = DataFrame()
        try:
            share_name = selector.xpath('//*[@id="_container_holder"]/table/tbody/tr/td[2]/div/div[2]/a/text()')
            share_proportion = selector.xpath('//*[@id="_container_holder"]/table/tbody/tr/td[3]/div/div/span/text()')
            share_contributive = selector.xpath('//*[@id="_container_holder"]/table/tbody/tr/td[4]/div/span/text()')
            share_contributive_tm = selector.xpath('//*[@id="_container_holder"]/table/tbody/tr/td[5]/div/span/text()')
            page = selector.xpath('//*[@id="_container_holder"]/div[@class="company_pager"]')
            pageNum = ''
            if page:
                pageNum = '1'
            share = {
                'share_name': share_name,
                'share_proportion': share_proportion,
                'share_contributive': share_contributive,
                'share_contributive_tm': share_contributive_tm,
                'pageNum': pageNum
            }
            share_data = DataFrame(share)
        except:
            pass
        item.share_data = share_data

        invest_data = DataFrame()
        try:
            name = selector.xpath('//*[@id="_container_invest"]/table/tbody/tr/td[2]/table/tr/td[2]/a/text()')
            btzper = selector.xpath('//*[@id="_container_invest"]/table/tbody/tr/td[3]/span/a/text()')
            reg_zb = selector.xpath('//*[@id="_container_invest"]/table/tbody/tr/td[4]/span/text()')
            invest_bl = selector.xpath('//*[@id="_container_invest"]/table/tbody/tr/td[5]/span/text()')
            reg_tm = selector.xpath('//*[@id="_container_invest"]/table/tbody/tr/td[6]/span/text()')
            status = selector.xpath('//*[@id="_container_invest"]/table/tbody/tr/td[7]/span/text()')
            page = selector.xpath('//*[@id="_container_invest"]/div/ul/li/a[@class="num -next"]/text()')
            # print(page)
            i = 2
            while page:
                res = self.session.get("https://www.tianyancha.com/pagination/invest.xhtml?pn=%s&id=%s"%(str(i),company_id),timeout=5).text
                selector2 = etree.HTML(res)
                page = selector2.xpath('/html/body/div/ul/li/a[@class="num -next"]/text()')
                i = i+1
                name1 = selector2.xpath('//table[@class="lazy-img  -alias -text -w36"]/tr/td[2]/a/text()')
                name = name+name1
                btzper1 = selector2.xpath('//table[@class="table"]/tbody/tr/td[3]/span/a/text()')
                btzper = btzper+btzper1
                reg_zb1 = selector2.xpath('//table[@class="table"]/tbody/tr/td[4]/span/text()')
                reg_zb = reg_zb+reg_zb1
                invest_bl1 = selector2.xpath('//table[@class="table"]/tbody/tr/td[5]/span/text()')
                invest_bl = invest_bl+invest_bl1
                reg_tm1 = selector2.xpath('//table[@class="table"]/tbody/tr/td[6]/span/text()')
                reg_tm = reg_tm + reg_tm1
                status1 = selector2.xpath('//table[@class="table"]/tbody/tr/td[7]/span/text()')
                status = status + status1
                if i > 10:
                    break
            invest = {
                'name_corp': name,
                'btzper': btzper,
                'reg_zb': reg_zb,
                'invest_bl': invest_bl,
                'reg_tm': reg_tm,
                'status': status,
            }
            invest_data = DataFrame(invest)
        except:
            pass
        item.invest_data=invest_data

        fenzhi_data = DataFrame()
        try:
            corp_name = selector.xpath('//*[@id="_container_branch"]/table/tbody/tr/td[2]/table/tr/td[2]/a/text()')
            fzren = selector.xpath('//*[@id="_container_branch"]/table/tbody/tr/td[3]/span/text()')
            reg_time = selector.xpath('//*[@id="_container_branch"]/table/tbody/tr/td[4]/span/text()')
            fz_status = selector.xpath('//*[@id="_container_branch"]/table/tbody/tr/td[5]/span/text()')
            page = selector.xpath('//*[@id="_container_branch"]/div/ul/li/a[@class="num -next"]/text()')
            i = 2
            while page:
                res = self.session.get("https://www.tianyancha.com/pagination/branch.xhtml?pn=%s&id=%s"%(str(i),company_id),timeout=5).text
                selector3 = etree.HTML(res)
                page = selector3.xpath('/html/body/div/ul/li/a[@class="num -next"]/text()')
                i = i+1
                corp_name1 = selector3.xpath('//table[@class="lazy-img -grow -alias -text -w36"]/tr/td[2]/a/text()')
                corp_name = corp_name +corp_name1
                fzren1 = selector3.xpath('//table[@class="table"]/tbody/tr/td[3]/span/text()')
                fzren = faren + fzren1
                reg_time1 = selector3.xpath('//table[@class="table"]/tbody/tr/td[4]/span/text()')
                reg_time = reg_time + reg_time1
                fz_status1 =selector3.xpath('//table[@class="table"]/tbody/tr/td[5]/span/text()')
                fz_status = fz_status+fz_status1
                if i>10:
                    break
            fenzhi = {
                'corp_name': corp_name,
                'fzren': fzren,
                'reg_time': reg_time,
                'fz_status': fz_status,
            }
            fenzhi_data = DataFrame(fenzhi)
        except:
            pass
        item.fenzhi_data = fenzhi_data

        biangengqian = selector.xpath('//*[@id="_container_changeinfo"]/table/tbody/tr/td[4]/div')
        biangengqian_li = []
        for i in biangengqian:
            i2 = i.xpath("string(.)")
            biangengqian_li.append(i2)
        biangenghou = selector.xpath('//*[@id="_container_changeinfo"]/table/tbody/tr/td[5]/div')
        biangenghou_li = []
        for r in biangenghou:
            r2 = r.xpath("string(.)")
            biangenghou_li.append(r2)
        change_data = DataFrame()
        try:
            change_tm = selector.xpath('//*[@id="_container_changeinfo"]/table/tbody/tr/td[2]/text()')
            change_project = selector.xpath('//*[@id="_container_changeinfo"]/table/tbody/tr/td[3]/text()')
            change_be = biangengqian_li
            change_af = biangenghou_li
            page = selector.xpath('//*[@id="_container_changeinfo"]/div/ul/li/a[@class="num -next"]/text()')
            # print(page)
            i = 2
            while page:
                res = self.session.get("https://www.tianyancha.com/pagination/changeinfo.xhtml?pn=%s&id=%s"%(str(i),company_id),timeout=5).text
                selector4 = etree.HTML(res)
                page = selector4.xpath('/html/body/div/ul/li/a[@class="num -next"]/text()')
                i = i+1
                change_tm1 = selector4.xpath('//table[@class="table"]/tbody/tr/td[2]/text()')
                change_tm = change_tm+change_tm1
                change_project1 = selector4.xpath('//table[@class="table"]/tbody/tr/td[3]/text()')
                change_project = change_project+change_project1
                change_be1 = selector4.xpath('//table[@class="table"]/tbody/tr/td[4]/div')
                cb1 = []
                for cb in change_be1:
                    c = cb.xpath("string(.)")
                    cb1.append(c)
                change_af1 = selector4.xpath('//table[@class="table"]/tbody/tr/td[5]/div')
                change_be = change_be+cb1
                ca1 = []
                for cb in change_af1:
                    c = cb.xpath("string(.)")
                    ca1.append(c)
                change_af = change_af+ca1
                if i>10:
                    break

            change = {
                'change_tm': change_tm,
                'change_project': change_project,
                'change_be': change_be,
                'change_af': change_af,
            }
            change_data = DataFrame(change)
        except:
            pass
        item.change_data = change_data

        Judicial_risk_data = DataFrame()
        try:
            hold_court_tm = selector.xpath('//*[@id="_container_announcementcourt"]/table/tbody/tr/td[2]/text()')
            Case = selector.xpath('//*[@id="_container_announcementcourt"]/table/tbody/tr/td[3]/span/text()')
            person = selector.xpath('//*[@id="_container_announcementcourt"]/table/tbody/tr/td[4]')
            per = []
            for i in person:
                r = i.xpath('string(.)')
                per.append(r)
            beigaoren = selector.xpath('//*[@id="_container_announcementcourt"]/table/tbody/tr/td[5]')
            bgr = []
            for i in beigaoren:
                r = i.xpath('string(.)')
                bgr.append(r)
            page = selector.xpath('//*[@id="_container_announcementcourt"]/div/ul/li/a[@class="num -next"]/text()')
            i = 2
            while page:
                res = self.session.get("https://www.tianyancha.com/pagination/announcementcourt.xhtml?pn=%s&id=%s"%(str(i),company_id),timeout=5).text
                selector5 = etree.HTML(res)
                page = selector5.xpath('/html/body/div/ul/li/a[@class="num -next"]/text()')
                i = i+1
                hold_court_tm1 = selector5.xpath('/html/body/table/tbody/tr/td[2]/text()')
                hold_court_tm = hold_court_tm+hold_court_tm1
                Case1 = selector5.xpath('/html/body/table/tbody/tr/td[3]/span/text()')
                Case = Case + Case1
                per1 = selector5.xpath('/html/body/table/tbody/tr/td[4]')
                p1 = []
                for p in per1:
                    pr = p.xpath('string(.)')
                    p1.append(pr)
                per = per+p1
                bgr1 = selector5.xpath('/html/body/table/tbody/tr/td[5]')
                b1 = []
                for b in bgr1:
                    br = b.xpath('string(.)')
                    b1.append(br)
                bgr = bgr + b1
                if i>10:
                    break

            Judicial_risk = {
                'hold_court_tm': hold_court_tm,
                'Case': Case,
                'person': per,
                'bgr': bgr,
            }
            Judicial_risk_data = DataFrame(Judicial_risk)
        except Exception as e:
            print(e)
            pass
        item.Judicial_risk_data = Judicial_risk_data

        legal_proceedings_data = DataFrame()
        try:
            tm = selector.xpath('//*[@id="_container_lawsuit"]/table/tbody/tr/td[2]/span/text()')
            documents = selector.xpath('//*[@id="_container_lawsuit"]/table/tbody/tr/td[3]/a/text()')
            case = selector.xpath('//*[@id="_container_lawsuit"]/table/tbody/tr/td[4]/span/text()')
            Case_identity = selector.xpath('//*[@id="_container_lawsuit"]/table/tbody/tr/td[5]')
            ci = []
            for i in Case_identity:
                r = i.xpath('string(.)')
                ci.append(r)
            case_num = selector.xpath('//*[@id="_container_lawsuit"]/table/tbody/tr/td[6]/span/text()')
            page = selector.xpath('//*[@id="_container_lawsuit"]/div/ul/li/a[@class="num -next"]/text()')
            i = 2
            while page:
                res = self.session.get('https://www.tianyancha.com/pagination/lawsuit.xhtml?pn=%s&name=%s'%(str(i),self.name),timeout=5).text
                selector6 = etree.HTML(res)
                page = selector6.xpath('/html/body/div/ul/li/a[@class="num -next"]/text()')
                i = i+1
                tm1 = selector6.xpath('/html/body/table/tbody/tr/td[2]/span/text()')
                tm = tm + tm1
                documents1 = selector6.xpath('/html/body/table/tbody/tr/td[3]/a/text()')
                documents = documents+documents1
                case1 = selector6.xpath('/html/body/table/tbody/tr/td[4]/span/text()')
                case = case+case1
                ci1 = selector6.xpath('/html/body/table/tbody/tr/td[5]')
                c1 = []
                for c in ci1:
                    c2 = c.xpath('string(.)')
                    c1.append(c2)
                ci = ci +c1
                case_num1 = selector6.xpath('/html/body/table/tbody/tr/td[6]/span/text()')
                case_num = case_num+case_num1
                if i > 10:
                    break
            legal_proceedings = {
                'tm': tm,
                'documents': documents,
                'case': case,
                'ci': ci,
                'case_num': case_num,
            }
            legal_proceedings_data = DataFrame(legal_proceedings)
        except Exception as e:
            pass
        item.legal_proceedings_data=legal_proceedings_data


        announcement_data = DataFrame()
        try:
            tm = selector.xpath('//*[@id="_container_court"]/table/tbody/tr/td[2]/text()')
            shangsufang = selector.xpath('//*[@id="_container_court"]/table/tbody/tr/td[3]/span')
            ssf = []
            for i in shangsufang:
                r = i.xpath('string(.)')
                ssf.append(r)
            beisufang = selector.xpath('//*[@id="_container_court"]/table/tbody/tr/td[4]/span')
            bsf = []
            for i in beisufang:
                r = i.xpath('string(.)')
                bsf.append(r)
            beigaoleixing = selector.xpath('//*[@id="_container_court"]/table/tbody/tr/td[5]/span/text()')
            court = selector.xpath('//*[@id="_container_court"]/table/tbody/tr/td[6]/span/text()')
            page = selector.xpath('//*[@id="_container_court"]/div/ul/li/a[@class="num -next"]/text()')
            i = 2
            while page:
                res = self.session.get("https://www.tianyancha.com/pagination/court.xhtml?pn=%s&name=%s"%(str(i),self.name),timeout=5).text
                selector7 = etree.HTML(res)
                page = selector7.xpath('/html/body/div/ul/li/a[@class="num -next"]/text()')
                i = i + 1
                tm1 = selector7.xpath('/html/body/table/tbody/tr/td[2]/text()')
                tm = tm +tm1
                shangsufang1 = selector7.xpath('/html/body/table/tbody/tr/td[3]')
                ssf1 = []
                for s in shangsufang1:
                    ss = s.xpath('string(.)')
                    if ss == "":
                        ss = "-"
                    ssf1.append(ss)
                ssf = ssf+ssf1
                beisufang1 = selector7.xpath('/html/body/table/tbody/tr/td[4]')
                bsf1 = []
                for bs in beisufang1:
                    b = bs.xpath('string(.)')
                    if b == "":
                        b = "-"
                    bsf1.append(b)
                bsf = bsf+bsf1
                beigaoleixing1 = selector7.xpath('/html/body/table/tbody/tr/td[5]/span/text()')
                beigaoleixing = beigaoleixing+beigaoleixing1
                court1 = selector7.xpath('/html/body/table/tbody/tr/td[6]/span/text()')
                court = court + court1

            announcement = {
                'tm': tm,
                'ssf': ssf,
                'bsf': bsf,
                'beigaoleixing': beigaoleixing,
                'court': court,
            }
            announcement_data = DataFrame(announcement)
        except:
            pass
        item.announcement_data = announcement_data

        Business_data = DataFrame()
        try:
            business_name = selector.xpath('//*[@id="_container_firmProduct"]/div/a[@class="product"]/div[@class="content"]/div[@class="title"]/text()')
            type = selector.xpath('//*[@id="_container_firmProduct"]/div/a/div[2]/div[@class="tag tag-new-category"]/text()')
            desc = selector.xpath('//*[@id="_container_firmProduct"]/div/a/div[2]/div[@class="desc"]/text()')
            busin_url = selector.xpath('//*[@id="_container_firmProduct"]/div/a[@class="product"]/@onclick')
            page = selector.xpath('//*[@id="_container_firmProduct"]/div[@class="company_pager"]')

            bus_keywords = []
            bus_des = []
            reg_tm = []
            Territoriality = []
            for u in busin_url:
                l = u[10:-2].split(",")[0][1:-1]
                url = "https://www.tianyancha.com/brand/%s" % (l)
                res1 = self.session.get(url,timeout=5).text
                # res1 = self.session.get(url, timeout=10).text
                # ,proxies=proxy
                se = etree.HTML(res1)
                keywords = se.xpath('//div[@class="tags"]/a/text()')
                keywords = str(keywords)[1:-1].replace("'", '')
                bus_keywords.append(keywords)
                reg_time = se.xpath('//span[@class="info"]/text()')[0].split('：')[1]
                reg_tm.append(reg_time)
                ter = se.xpath('//span[@class="info"]/text()')[1].split('：')[1]
                Territoriality.append(ter)
                des = se.xpath('//*[@id="_container_desc"]/text()')[0]
                bus_des.append(des)
            business = {
                'business_name': business_name,
                'type': type,
                'desc': desc,
                'bus_keywords': bus_keywords,
                'bus_des': bus_des,
                'reg_tm': reg_tm,
                'Territoriality': Territoriality,
            }
            Business_data = DataFrame(business)
        except:
            pass
        item.Business_data = Business_data

        inve_event_data = DataFrame()
        try:
            tm = selector.xpath('//*[@id="_container_touzi"]/table/tbody/tr/td[2]/text()')
            lunci = selector.xpath('//*[@id="_container_touzi"]/table/tbody/tr/td[3]/text()')
            jine = selector.xpath('//*[@id="_container_touzi"]/table/tbody/tr/td[4]/text()')
            touzifang = selector.xpath('//*[@id="_container_touzi"]/table/tbody/tr/td[5]')
            tzf = []
            for n in touzifang:
                t = n.xpath('string(.)')
                tzf.append(t)
            product = selector.xpath('//*[@id="_container_touzi"]/table/tbody/tr/td[6]/table/tr/td[2]/a/text()')
            diqu = selector.xpath('//*[@id="_container_touzi"]/table/tbody/tr/td[7]/text()')
            ins = selector.xpath('//*[@id="_container_touzi"]/table/tbody/tr/td[8]/a/text()')
            busi = selector.xpath('//*[@id="_container_touzi"]/table/tbody/tr/td[9]/text()')
            page = selector.xpath('//*[@id="_container_touzi"]/div[@class="company_pager"]')
            pageNum = ''
            if page:
                pageNum = '1'
            inve_event = {
                'tm': tm,
                'lunci': lunci,
                'jine': jine,
                'tzf': tzf,
                'product1': product,
                'diqu': diqu,
                'ins': ins,
                'busi': busi,
                'pageNum': pageNum
            }
            inve_event_data = DataFrame(inve_event)
        except:
            pass
        # print(inve_event_data)
        item.inve_event_data = inve_event_data

        Financing_data = DataFrame()
        try:
            tm = selector.xpath('//*[@id="_container_rongzi"]/table/tbody/tr/td[2]/text()')
            rotation = selector.xpath('//*[@id="_container_rongzi"]/table/tbody/tr/td[3]/text()')
            valuation = selector.xpath('//*[@id="_container_rongzi"]/table/tbody/tr/td[4]/text()')
            Amount_of_money = selector.xpath('//*[@id="_container_rongzi"]/table/tbody/tr/td[5]/text()')
            bili = selector.xpath('//*[@id="_container_rongzi"]/table/tbody/tr/td[6]/text()')
            Investor = selector.xpath('//*[@id="_container_rongzi"]/table/tbody/tr/td[7]')
            page = selector.xpath('//*[@id="_container_rongzi"]/div[@class="company_pager"]')
            pageNum = ''
            if page:
                pageNum = '1'
            Investors = []
            for i in Investor:
                r = i.xpath('string(.)')
                Investors.append(r)
            newsly = selector.xpath('//*[@id="_container_rongzi"]/table/tbody/tr/td[8]')
            newslys = []
            for i in newsly:
                r = i.xpath('string(.)')
                newslys.append(r)
            Financing = {
                'tm':tm,
                'rotation': rotation,
                'valuation': valuation,
                'Amount_of_money': Amount_of_money,
                'bili': bili,
                'Investors': Investors,
                'newslys': newslys,
                'pageNum': pageNum
            }
            Financing_data = DataFrame(Financing)
        except:
            pass
        item.Financing_data = Financing_data

        administrative_licensing_data = DataFrame()
        try:
            xukebianhao = selector.xpath('//*[@id="_container_licensing"]/table/tbody/tr/td[2]/text()')
            xukename = selector.xpath('//*[@id="_container_licensing"]/table/tbody/tr/td[3]/text()')
            youxiaoqizi = selector.xpath('//*[@id="_container_licensing"]/table/tbody/tr/td[4]/text()')
            youxiaoqizhi = selector.xpath('//*[@id="_container_licensing"]/table/tbody/tr/td[5]/text()')
            xukejiguan = selector.xpath('//*[@id="_container_licensing"]/table/tbody/tr/td[6]/text()')
            xukeneirong = selector.xpath('//*[@id="_container_licensing"]/table/tbody/tr/td[7]/text()')
            administrative_licensing = {
                'xukebianhao': xukebianhao,
                'xukename': xukename,
                'youxiaoqizi': youxiaoqizi,
                'youxiaoqizhi': youxiaoqizhi,
                'xukejiguan': xukejiguan,
                'xukeneirong': xukeneirong,
            }
            administrative_licensing_data = DataFrame(administrative_licensing)
        except:
            pass
        item.administrative_licensing_data = administrative_licensing_data

        Tax_data = DataFrame()
        try:
            tm = selector.xpath('//*[@id="_container_taxcredit"]/table/tbody/tr/td[2]/text()')
            tax_rating = selector.xpath('//*[@id="_container_taxcredit"]/table/tbody/tr/td[3]/text()')
            type = selector.xpath('//*[@id="_container_taxcredit"]/table/tbody/tr/td[4]/text()')
            Taxpayer_id = selector.xpath('//*[@id="_container_taxcredit"]/table/tbody/tr/td[5]/text()')
            evaluation_unit = selector.xpath('//*[@id="_container_taxcredit"]/table/tbody/tr/td[6]/text()')
            page = selector.xpath('//*[@id="_container_taxcredit"]/div[@class="company_pager"]')
            tax = {
                'tm': tm,
                'tax_rating': tax_rating,
                'type': type,
                'Taxpayer_id': Taxpayer_id,
                'evaluation_unit': evaluation_unit,
            }
            Tax_data = DataFrame(tax)
        except:
            pass
        item.Tax_data = Tax_data

        Qualification_certificate = DataFrame()
        try:
            certificate = selector.xpath('//*[@id="_container_certificate"]/table/tbody/tr/td[2]/span/text()')
            certificate_id = selector.xpath('//*[@id="_container_certificate"]/table/tbody/tr/td[3]/span/text()')
            fazhengriqi = selector.xpath('//*[@id="_container_certificate"]/table/tbody/tr/td[4]/span/text()')
            jiezhiriqi = selector.xpath('//*[@id="_container_certificate"]/table/tbody/tr/td[5]/span/text()')
            page = selector.xpath('//*[@id="_container_taxcredit"]/div[@class="company_pager"]')
            pageNum = ''
            if page:
                pageNum = '1'
            Qualification = {
                'certificate': certificate,
                'certificate_id': certificate_id,
                'fazhengriqi': fazhengriqi,
                'jiezhiriqi': jiezhiriqi,
                'pageNum': pageNum
            }
            Qualification_certificate = DataFrame(Qualification)
        except:
            pass
        item.Qualification_certificate = Qualification_certificate

        Bidding_data = DataFrame()
        try:
            tm = selector.xpath('//*[@id="_container_bid"]/table/tbody/tr/td[2]/text()')
            title = selector.xpath('//*[@id="_container_bid"]/table/tbody/tr/td[3]/a/text()')
            person = selector.xpath('//*[@id="_container_bid"]/table/tbody/tr/td[4]/text()')
            page = selector.xpath('//*[@id="_container_bid"]/div[@class="company_pager"]')
            pageNum = ''
            if page:
                pageNum = '1'
            Bidding = {
                'tm': tm,
                'title': title,
                'person': person,
                'pageNum': pageNum
            }
            Bidding_data = DataFrame(Bidding)
        except:
            pass
        item.Bidding_data = Bidding_data

        im_ex_credit = DataFrame()
        try:
            haiguan = selector.xpath('//*[@id="_container_importAndExport"]/table/tbody/tr/td[1]/text()')
            haiguanbianma = selector.xpath('//*[@id="_container_importAndExport"]/table/tbody/tr/td[2]/text()')
            type = selector.xpath('//*[@id="_container_importAndExport"]/table/tbody/tr/td[3]/text()')
            page = selector.xpath('//*[@id="_container_importAndExport"]/div[@class="company_pager"]')
            pageNum = ''
            if page:
                pageNum = '1'
            im_ex = {
                'haiguan': haiguan,
                'haiguanbianma': haiguanbianma,
                'type': type,
                'pageNum': pageNum
            }
            im_ex_credit = DataFrame(im_ex)
        except:
            pass
        item.im_ex_credit = im_ex_credit

        Trademark_data = DataFrame()
        try:
            reg_tm = selector.xpath('//*[@id="_container_tmInfo"]/div[2]/table/tbody/tr/td[2]/span/text()')
            name = selector.xpath('//*[@id="_container_tmInfo"]/div[2]/table/tbody/tr/td[4]/span/text()')
            reg_id = selector.xpath('//*[@id="_container_tmInfo"]/div[2]/table/tbody/tr/td[5]/span/text()')
            type = selector.xpath('//*[@id="_container_tmInfo"]/div[2]/table/tbody/tr/td[6]/span/text()')
            process_state = selector.xpath('//*[@id="_container_tmInfo"]/div[2]/table/tbody/tr/td[7]/span/text()')
            page = selector.xpath('//*[@id="_container_tmInfo"]/div[2]/div/ul/li/a[@class="num -next"]/text()')
            i = 2
            while page:
                res=self.session.get('https://www.tianyancha.com/pagination/tmInfo.xhtml?pn=%s&id=%s'%(str(i),company_id),timeout=5).text
                # print(res)
                selector8 = etree.HTML(res)
                page = selector8.xpath('/html/body/div/ul/li/a[@class="num -next"]/text()')
                i = i+1
                reg_tm1 = selector8.xpath('/html/body/div[2]/table/tbody/tr/td[2]/span/text()')
                reg_tm = reg_tm+reg_tm1
                name1 = selector8.xpath('/html/body/div[2]/table/tbody/tr/td[4]/span/text()')
                name = name+name1
                reg_id1 = selector8.xpath('/html/body/div[2]/table/tbody/tr/td[5]/span/text()')
                reg_id = reg_id+reg_id1
                type1 = selector8.xpath('/html/body/div[2]/table/tbody/tr/td[6]/span/text()')
                type = type +type1
                process_state1 = selector8.xpath('/html/body/div[2]/table/tbody/tr/td[7]/span/text()')
                process_state = process_state + process_state1
                if i > 10:
                    break
            pageNum = ''
            if page:
                pageNum = '1'
            Trademark = {
                'reg_tm': reg_tm,
                'name': name,
                'reg_id': reg_id,
                'type': type,
                'process_state': process_state,
                'pageNum': pageNum
            }
            Trademark_data = DataFrame(Trademark)
        except:
            pass
        item.Trademark_data=Trademark_data

        Copyright_data = DataFrame()
        try:
            tm = selector.xpath('//*[@id="_container_copyright"]/table/tbody/tr/td[2]/span/text()')
            name = selector.xpath('//*[@id="_container_copyright"]/table/tbody/tr/td[3]/span/text()')
            # print(name)
            abbreviation = selector.xpath('//*[@id="_container_copyright"]/table/tbody/tr/td[4]/span/text()')
            register = selector.xpath('//*[@id="_container_copyright"]/table/tbody/tr/td[5]/span/text()')
            type_id = selector.xpath('//*[@id="_container_copyright"]/table/tbody/tr/td[6]/span/text()')
            version = selector.xpath('//*[@id="_container_copyright"]/table/tbody/tr/td[7]/span/text()')
            page = selector.xpath('//*[@id="_container_copyright"]/div/ul/li/a[@class="num -next"]/text()')
            i = 2
            while page:
                res = self.session.get("https://www.tianyancha.com/pagination/copyright.xhtml?pn=%s&id=%s"%(str(i),company_id),timeout=5).text
                selector9 = etree.HTML(res)
                page = selector9.xpath('/html/body/div/ul/li/a[@class="num -next"]/text()')
                i = i+1
                tm1 = selector9.xpath('/html/body/table/tbody/tr/td[2]/span/text()')
                tm = tm +tm1
                name1 = selector9.xpath('/html/body/table/tbody/tr/td[3]/span/text()')
                name = name+name1
                abbreviation1 = selector9.xpath('/html/body/table/tbody/tr/td[4]/span/text()')
                abbreviation = abbreviation+abbreviation1
                register1 = selector9.xpath('/html/body/table/tbody/tr/td[5]/span/text()')
                register = register +register1
                type_id1 = selector9.xpath('/html/body/table/tbody/tr/td[6]/span/text()')
                type_id = type_id+type_id1
                version1 = selector9.xpath('/html/body/table/tbody/tr/td[7]/span/text()')
                version = version+version1
                if i>10:
                    break
            copyright = {
                'tm': tm,
                'name': name,
                'abbreviation': abbreviation,
                'register': register,
                'type_id': type_id,
                'version': version,
            }
            Copyright_data = DataFrame(copyright)
            # print(Copyright_data)
        except:
            pass
        item.Copyright_data = Copyright_data

        works_data = DataFrame()
        try:
            works_name = selector.xpath('//*[@id="_container_copyrightWorks"]/table/tbody/tr/td[2]/span/text()')
            reg_id = selector.xpath('//*[@id="_container_copyrightWorks"]/table/tbody/tr/td[3]/span/text()')
            type = selector.xpath('//*[@id="_container_copyrightWorks"]/table/tbody/tr/td[4]/span/text()')
            complete_date = selector.xpath('//*[@id="_container_copyrightWorks"]/table/tbody/tr/td[5]/span/text()')
            red_date = selector.xpath('//*[@id="_container_copyrightWorks"]/table/tbody/tr/td[6]/span/text()')
            first_date = selector.xpath('//*[@id="_container_copyrightWorks"]/table/tbody/tr/td[7]/span/text()')
            page = selector.xpath('//*[@id="_container_copyrightWorks"]/div/ul/li/a[@class="num -next"]/text()')
            i = 2
            while page:
                res = self.session.get("https://www.tianyancha.com/pagination/copyrightWorks.xhtml?pn=%s&id=%s"%(str(i),company_id),timeout=5).text
                selector10 = etree.HTML(res)
                page = selector10.xpath('/html/body/div/ul/li/a[@class="num -next"]/text()')
                i = i+1
                works_name1 = selector10.xpath('/html/body/table/tbody/tr/td[2]/span/text()')
                works_name = works_name+works_name1
                reg_id1 =selector10.xpath('/html/body/table/tbody/tr/td[3]/span/text()')
                reg_id = reg_id+reg_id1
                type1 = selector10.xpath('/html/body/table/tbody/tr/td[4]/span/text()')
                type = type + type1
                complete_date1 = selector10.xpath('/html/body/table/tbody/tr/td[5]/span/text()')
                complete_date = complete_date+complete_date1
                red_date1 = selector10.xpath('/html/body/table/tbody/tr/td[6]/span/text()')
                red_date = red_date+red_date1
                first_date1=selector10.xpath('/html/body/table/tbody/tr/td[7]/span/text()')
                first_date = first_date+first_date1
            works = {
                'works_name': works_name,
                'reg_id': reg_id,
                'type': type,
                'complete_date': complete_date,
                'red_date': red_date,
                'first_date': first_date,

            }
            works_data = DataFrame(works)
        except:
            pass
        item.works_data = works_data

        Record_data = DataFrame()
        try:
            examine_tm = selector.xpath('//*[@id="_container_icp"]/table/tbody/tr/td[2]/span/text()')
            website_name = selector.xpath('//*[@id="_container_icp"]/table/tbody/tr/td[3]/span/text()')
            host_page = selector.xpath('//*[@id="_container_icp"]/table/tbody/tr/td[4]/a/@href')
            domain_name = selector.xpath('//*[@id="_container_icp"]/table/tbody/tr/td[5]/text()')
            record = selector.xpath('//*[@id="_container_icp"]/table/tbody/tr/td[6]/span/text()')
            status = selector.xpath('//*[@id="_container_icp"]/table/tbody/tr/td[7]/span/text()')
            nature = selector.xpath('//*[@id="_container_icp"]/table/tbody/tr/td[8]/span/text()')
            page = selector.xpath('//*[@id="_container_icp"]/div[@class="company_pager"]')
            pageNum = ''
            if page:
                pageNum = '1'
            record_d = {
                'examine_tm': examine_tm,
                'website_name': website_name,
                'host_page': host_page,
                'domain_name': domain_name,
                'record': record,
                'status': status,
                'nature': nature,
                'pageNum': pageNum
            }
            Record_data = DataFrame(record_d)
        except:
            pass
        item.Record_data = Record_data
        item.weichat=[]
        try:
            weixinName = selector.xpath('//*[@class="wechat"]/div[@class="content"]/div/text()')
            weixinhao = selector.xpath('//*[@class="wechat"]/div[@class="content"]/div[2]/span[2]/text()')
            gongneng = selector.xpath('//*[@class="wechat"]/div[@class="content"]/div[3]/span[2]/text()')
            weichat = []
            for i in range(0,len(weixinName)):
                weixin = {
                    'weixinName':weixinName[i],
                    'weixinhao':weixinhao[i],
                    'gongneng':gongneng[i]
                }
                data = json.dumps(weixin, ensure_ascii=False)
                weichat.append(data)
            item.weichat = weichat
        except:
            pass

        item.patents = []
        try:
            sqtime = selector.xpath('//*[@id="_container_patent"]/table/tbody/tr/td[2]/span/text()')
            zlname = selector.xpath('//*[@id="_container_patent"]/table/tbody/tr/td[3]/span/text()')
            sqnum = selector.xpath('//*[@id="_container_patent"]/table/tbody/tr/td[4]/span/text()')
            sqgbnum = selector.xpath('//*[@id="_container_patent"]/table/tbody/tr/td[5]/span/text()')
            zltype = selector.xpath('//*[@id="_container_patent"]/table/tbody/tr/td[6]/span/text()')
            page = selector.xpath('//*[@id="_container_patent"]/div/ul/li/a[@class="num -next"]/text()')
            i = 2
            while page:
                res = self.session.get('https://www.tianyancha.com/pagination/patent.xhtml?pn=%s&id=%s'%(i,company_id),timeout=5).text
                selector12 = etree.HTML(res)
                page = selector12.xpath('/html/body/div/ul/li/a[@class="num -next"]/text()')
                i = i+1
                sqtime1 = selector12.xpath('/html/body/table/tbody/tr/td[2]/span/text()')
                zlname1 = selector12.xpath('/html/body/table/tbody/tr/td[3]/span/text()')
                sqnum1 = selector12.xpath('/html/body/table/tbody/tr/td[4]/span/text()')
                sqgbnum1 = selector12.xpath('/html/body/table/tbody/tr/td[5]/span/text()')
                zltype1 = selector12.xpath('/html/body/table/tbody/tr/td[6]/span/text()')
                sqtime = sqtime+sqtime1
                zlname = zlname+zlname1
                sqnum = sqnum+sqnum1
                sqgbnum = sqgbnum +sqgbnum1
                zltype = zltype+zltype1
            patents=[]
            for i in range(0,len(zlname)):
                patent = {
                    'sqtime':sqtime[i],
                    'zlname':zlname[i],
                    'sqnum':sqnum[i],
                    'sqgbnum':sqgbnum[i],
                    'zltype':zltype[i]
                }
                data = json.dumps(patent, ensure_ascii=False)
                patents.append(data)
            item.patents=patents
        except:
            pass
        item.xinyongzgs = []
        try:
            wsh = selector.xpath('//*[@id="_container_licensingXyzg"]/table/tbody/tr/td[2]/text()')
            xkjg = selector.xpath('//*[@id="_container_licensingXyzg"]/table/tbody/tr/td[3]/text()')
            xktm = selector.xpath('//*[@id="_container_licensingXyzg"]/table/tbody/tr/td[4]/text()')
            xinyongzgs = []
            for i in range(0,len(wsh)):
                xinyongzg = {
                    'wsh':wsh[i],
                    'xkjg':xkjg[i],
                    'xktm':xktm
                }
                data = json.dumps(xinyongzg, ensure_ascii=False)
                xinyongzgs.append(data)
            item.xinyongzgs = xinyongzgs
        except:
            pass
        item.hexin = []
        try:
            name = selector.xpath('//*[@id="_container_teamMember"]/div/div/div[1]/div[2]')
            names = []
            for n in name:
                na = n.xpath('string(.)')
                names.append(na)
            zhiwei = selector.xpath('//*[@id="_container_teamMember"]/div/div/div[2]/div/text()')
            jianjie = selector.xpath('//*[@id="_container_teamMember"]/div/div/div[2]/p[1]/text()')
            hexin = []
            for i in range(0,len(names)):
                hexin = {
                    'name':names[i],
                    'zhiwei':zhiwei,
                    'jianjie':jianjie
                }
                data = json.dumps(hexin, ensure_ascii=False)
                hexin.append(data)
            item.hexin = hexin
        except:
            pass

        item.chufa = []
        try:
            tm = selector.xpath('//*[@id="_container_punish"]/table/tbody/tr/td[2]/text()')
            juedingwenshui = selector.xpath('//*[@id="_container_punish"]/table/tbody/tr/td[3]/text()')
            leixin = selector.xpath('//*[@id="_container_punish"]/table/tbody/tr/td[4]/text()')
            juedingjiguan = selector.xpath('//*[@id="_container_punish"]/table/tbody/tr/td[5]/text()')
            chufas = []
            for i in range(0,len(tm)):
                cchufa={
                    'tm':tm,
                    'juedingwenshui':juedingwenshui,
                    'leixin':leixin,
                    'jueidngjiguan':juedingjiguan
                }
                data = json.dumps(cchufa, ensure_ascii=False)
                chufas.append(data)
            item.chufa = chufas
        except Exception as e:
            print(e)
            pass

        item.zuizhongshouyiren = []
        try:
            name = selector.xpath('//*[@id="_container_humanholding"]/table/tbody/tr/td[2]/span/a/text()')
            chigubili = selector.xpath('//*[@id="_container_humanholding"]/table/tbody/tr/td[3]/span/text()')
            guquanlian = selector.xpath('//*[@id="_container_humanholding"]/table/tbody/tr/td[4]/div')
            guquanlians = []
            for i in guquanlian:
                guquan = i.xpath('string(.)')
                guquanlians.append(guquan)
            shouyi = []
            for z in range(0,len(name)):
                zzsy = {
                    'name':name[i],
                    'chigubili':chigubili[i],
                    'guquanlians':guquanlians[i]
                }
                data = json.dumps(zzsy, ensure_ascii=False)
                shouyi.append(data)
            item.zuizhongshouyiren = shouyi
        except:
            pass

        regtm = str(regtm)[2:-2]
        item.regtm = regtm
        item.zhuceshijian = ''
        try:
            item.zhuceshijian = regtm.split("至")[0]
        except:
            pass
        try:
            item.jianjie = jianjie[0].strip()
        except:
            pass
        item.diqu =''
        item.jyfw = str(jyfw)[2:-2]
        item.tongyixinyongdaima = '-'
        item.faren = str(faren)[2:-2]
        item.phone = str(phone)[2:-2]
        item.email = str(email)[2:-2]
        item.guanwang = str(guanwang)[2:-2]
        item.dizhi = str(dizhi)[2:-2]
        item.gongshangzhuce = str(gongshangzhuce)[2:-2]
        item.zuzhijigoudaima = str(zuzhijigoudaima)[2:-2]
        item.tongyixinyongdaima = str(tongyixinyongdaima)[2:-2]
        item.nashuirenshibiehao= str(nashuirenshibiehao)[2:-2]
        item.comp_type = str(comp_type)[2:-2]
        item.hangye = str(hangye)[2:-2]
        item.zhucedizhi = str(zhucedizhi)[2:-2]
        item.dengjijiguan = str(dengjijiguan)[2:-2]
        item.yingwenming = str(yingwenming)[2:-2]
        item.product_des = str(product_des)[2:-2]
        item.hezhunriqi = str(hezhunriqi)[2:-2]
        item.zhuceziben = str(zhuceziben)[2:-2]
        item.jystatus = str(jystatus)[2:-2]

        return item


if __name__ == '__main__':
    t = Tianyancah("腾讯")
    item = t.get_list()
    mainper = []
    sh = []
    inv = []
    branch = []
    changeData = []
    judicial_risk_data = []
    legal_proceedings_data = []
    announcement = []
    business = []
    inveEvent = []
    financing = []
    administrativeLicensing = []
    qualificationCertificate = []
    biddingData = []
    im_ex_credit = []
    trademarkData = []
    copyrightData = []
    worksData = []
    recordData = []
    taxData = []
    try:
        for i in range(0, item.main_per_data.shape[0]):
            ma = {
                'personName': item.main_per_data.loc[i].main_per_name,
                'position': item.main_per_data.loc[i].main_per_posit,
            }
            ma = json.dumps(ma, ensure_ascii=False)
            mainper.append(ma)
    except Exception as e:
        print(e)
    try:
        for i in range(0, item.share_data.shape[0]):
            share = {
                'shareholderName': item.share_data.loc[i].share_name,
                'proportion': item.share_data.loc[i].share_proportion,
                'contributive': item.share_data.loc[i].share_contributive,
                'contributiveTm': item.share_data.loc[i].share_contributive_tm,
                'pageNum': item.main_per_data.loc[i].pageNum
            }
            share = json.dumps(share, ensure_ascii=False)
            sh.append(share)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.invest_data.shape[0]):
            invest = {
                'corpName': item.invest_data.loc[i].name_corp,
                'legalPerson': item.invest_data.loc[i].btzper,
                'capital': item.invest_data.loc[i].reg_zb,
                'investmentRatio': item.invest_data.loc[i].invest_bl,
                'regTm': item.invest_data.loc[i].reg_tm,
                'status': item.invest_data.loc[i].status,
            }
            invest = json.dumps(invest, ensure_ascii=False)
            inv.append(invest)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.fenzhi_data.shape[0]):
            fz = {
                'corpName': item.fenzhi_data.loc[i].corp_name,
                'person': item.fenzhi_data.loc[i].fzren,
                'regTm': item.fenzhi_data.loc[i].reg_time,
                'status': item.fenzhi_data.loc[i].fz_status,
            }
            fz = json.dumps(fz, ensure_ascii=False)
            branch.append(fz)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.change_data.shape[0]):
            change = {
                'changeTm': item.change_data.loc[i].change_tm,
                'changeProject': item.change_data.loc[i].change_project,
                'changeBe': item.change_data.loc[i].change_be,
                'changeAf': item.change_data.loc[i].change_af,
            }
            change = json.dumps(change, ensure_ascii=False)
            changeData.append(change)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.Judicial_risk_data.shape[0]):
            # Judicial_risk_data
            judicial = {
                'holdCourtTm': item.Judicial_risk_data.loc[i].hold_court_tm,
                'judicialCase': item.Judicial_risk_data.loc[i].Case,
                'person': item.Judicial_risk_data.loc[i].person,
                'bgr': item.Judicial_risk_data.loc[i].bgr,
            }
            judicial = json.dumps(judicial, ensure_ascii=False)
            judicial_risk_data.append(judicial)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.legal_proceedings_data.shape[0]):
            legal_proceedings = {
                'tm': item.legal_proceedings_data.loc[i].tm,
                'documents': item.legal_proceedings_data.loc[i].documents,
                'legalProceedingsCase': item.legal_proceedings_data.loc[i].case,
                'ci': item.legal_proceedings_data.loc[i].ci,
                'caseNum': item.legal_proceedings_data.loc[i].case_num
            }
            legal_proceedings = json.dumps(legal_proceedings, ensure_ascii=False)
            legal_proceedings_data.append(legal_proceedings)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.announcement_data.shape[0]):
            announcement_data = {
                'tm': item.announcement_data.loc[i].tm,
                'ssf': item.announcement_data.loc[i].ssf,
                'bsf': item.announcement_data.loc[i].bsf,
                'beigaoleixing': item.announcement_data.loc[i].beigaoleixing,
                'court': item.announcement_data.loc[i].court
            }
            announcement_data = json.dumps(announcement_data, ensure_ascii=False)
            announcement.append(announcement_data)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.Business_data.shape[0]):
            business_data = {
                'businessName': item.Business_data.loc[i].business_name,
                'type': item.Business_data.loc[i].type,
                'desc': item.Business_data.loc[i].desc,
                'busKeywords': item.Business_data.loc[i].bus_des,
                'busDes': item.Business_data.loc[i].bus_keywords,
                'regTm': item.Business_data.loc[i].reg_tm,
                'territoriality': item.Business_data.loc[i].Territoriality,
            }
            business_data = json.dumps(business_data, ensure_ascii=False)
            business.append(business_data)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.inve_event_data.shape[0]):
            inve_event_data = {
                'tm': item.inve_event_data.loc[i].tm,
                'lunci': item.inve_event_data.loc[i].lunci,
                'jine': item.inve_event_data.loc[i].jine,
                'tzf': item.inve_event_data.loc[i].tzf,
                'product': item.inve_event_data.loc[i].product1,
                'diqu': item.inve_event_data.loc[i].diqu,
                'ins': item.inve_event_data.loc[i].ins,
                'busi': item.inve_event_data.loc[i].busi,
            }
            inve_event_data = json.dumps(inve_event_data, ensure_ascii=False)
            inveEvent.append(inve_event_data)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.Financing_data.shape[0]):
            financingData = {
                'tm': item.Financing_data.loc[i].tm,
                'rotation': item.Financing_data.loc[i].rotation,
                'valuation': item.Financing_data.loc[i].valuation,
                'AmountOfMoney': item.Financing_data.loc[i].Amount_of_money,
                'bili': item.Financing_data.loc[i].bili,
                'investors': item.Financing_data.loc[i].Investors,
                'newslys': item.Financing_data.loc[i].newslys
            }
            financingData = json.dumps(financingData, ensure_ascii=False)
            financing.append(financingData)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.administrative_licensing_data.shape[0]):
            administrative_licensing_data = {
                'xukebianhao': item.administrative_licensing_data.loc[i].xukebianhao,
                'xukename': item.administrative_licensing_data.loc[i].xukename,
                'youxiaoqizi': item.administrative_licensing_data.loc[i].youxiaoqizi,
                'youxiaoqizhi': item.administrative_licensing_data.loc[i].youxiaoqizhi,
                'xukejiguan': item.administrative_licensing_data.loc[i].xukejiguan,
                'xukeneirong': item.administrative_licensing_data.loc[i].xukeneirong,
            }
            administrative_licensing_data = json.dumps(administrative_licensing_data, ensure_ascii=False)
            administrativeLicensing.append(administrative_licensing_data)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.Tax_data.shape[0]):
            tax = {
                'tm': item.Tax_data.loc[i].tm,
                'taxRating': item.Tax_data.loc[i].tax_rating,
                'type': item.Tax_data.loc[i].type,
                'TaxpayerId': item.Tax_data.loc[i].Taxpayer_id,
                'evaluationUnit': item.Tax_data.loc[i].evaluation_unit
            }
            tax = json.dumps(tax, ensure_ascii=False)
            taxData.append(tax)

    except Exception as e:
        print(e)

    try:
        for i in range(0, item.Qualification_certificate.shape[0]):
            qualification_Certificate = {
                'certificate': item.Qualification_certificate.loc[i].certificate,
                'certificateId': item.Qualification_certificate.loc[i].certificate_id,
                'fazhengriqi': item.Qualification_certificate.loc[i].fazhengriqi,
                'jiezhiriqi': item.Qualification_certificate.loc[i].jiezhiriqi,
            }
            qualification_Certificate = json.dumps(qualification_Certificate, ensure_ascii=False)
            qualificationCertificate.append(qualification_Certificate)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.Bidding_data.shape[0]):
            Bidding_Data = {
                'tm': item.Bidding_data.loc[i].tm,
                'title': item.Bidding_data.loc[i].title,
                'person': item.Bidding_data.loc[i].person,
            }
            Bidding_Data = json.dumps(Bidding_Data, ensure_ascii=False)
            biddingData.append(Bidding_Data)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.im_ex_credit.shape[0]):
            im_ex = {
                'haiguan': item.im_ex_credit.loc[i].haiguan,
                'haiguanbianma': item.im_ex_credit.loc[i].haiguanbianma,
                'type': item.im_ex_credit.loc[i].type,
            }
            im_ex1 = json.dumps(im_ex, ensure_ascii=False)
            im_ex_credit.append(im_ex1)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.Trademark_data.shape[0]):
            Trademark_data = {
                'regTm': item.Trademark_data.loc[i].reg_tm,
                'name': item.Trademark_data.loc[i].name,
                'regId': item.Trademark_data.loc[i].reg_id,
                'type': item.Trademark_data.loc[i].type,
                'processState': item.Trademark_data.loc[i].process_state,
            }
            Trademark_data = json.dumps(Trademark_data, ensure_ascii=False)
            trademarkData.append(Trademark_data)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.Copyright_data.shape[0]):
            Copyright_data = {
                'tm': item.Copyright_data.loc[i].tm,
                'name': item.Copyright_data.loc[i].name,
                'abbreviation': item.Copyright_data.loc[i].abbreviation,
                'register': item.Copyright_data.loc[i].register,
                'typeId': item.Copyright_data.loc[i].type_id,
                'version': item.Copyright_data.loc[i].version
            }
            Copyright_data = json.dumps(Copyright_data, ensure_ascii=False)
            copyrightData.append(Copyright_data)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.works_data.shape[0]):
            works_data = {
                'worksName': item.works_data.loc[i].works_name,
                'regId': item.works_data.loc[i].reg_id,
                'type': item.works_data.loc[i].type,
                'completeDate': item.works_data.loc[i].complete_date,
                'redDate': item.works_data.loc[i].red_date,
                'firstDate': item.works_data.loc[i].first_date,
            }
            works_data = json.dumps(works_data, ensure_ascii=False)
            worksData.append(works_data)
    except Exception as e:
        print(e)

    try:
        for i in range(0, item.Record_data.shape[0]):
            Record_data = {
                'examineTm': item.Record_data.loc[i].examine_tm,
                'websiteName': item.Record_data.loc[i].website_name,
                'hostNage': item.Record_data.loc[i].host_page,
                'domainName': item.Record_data.loc[i].domain_name,
                'record': item.Record_data.loc[i].record,
                'status': item.Record_data.loc[i].status,
                'nature': item.Record_data.loc[i].nature
            }
            Record_data = json.dumps(Record_data, ensure_ascii=False)
            recordData.append(Record_data)
    except Exception as e:
        print(e)
    data = ''
    try:
        comp = {
            'companyName': item.name,
            'corpCode': item.tongyixinyongdaima,
            'organizingInstitutionBarCode': item.zuzhijigoudaima,
            'industryAndCommerce': item.gongshangzhuce,
            'identificationNumberOfTheTaxpayer': item.nashuirenshibiehao,
            'operatingPeriod': item.regtm,
            'checkAndApprove': item.hezhunriqi,
            'registrationAuthority': item.dengjijiguan,
            'registeredAssets': item.zhuceziben,
            'jystatus': item.jystatus,
            'renyuanguimo': item.renyuanguimo,
            'EnglishName': item.yingwenming,
            'nashuirenzizhi': item.nashuirenzizhi,
            'shijiaoziben': item.shijiaoziben,
            'corpType': item.comp_type,
            'corpDesc': item.jianjie,
            'legalPerson': item.faren,
            'Phone': item.phone,
            'Email': item.email,
            'corpHomePag': item.guanwang,
            'address': item.dizhi,
            'area': item.diqu,
            'regTm': item.zhuceshijian,
            'industry': item.hangye,
            'scopeOfBusiness': item.jyfw,
            'corpProduct': item.product,
            'corpKeywords': item.keyword,
            'corpProduct_Desc': item.product_des,
            'updateTm': str(datetime.datetime.now())[:-3],
            'mainPerson': mainper,
            'share': sh,
            'invest': inv,
            'branch': branch,
            'changeData': changeData,
            'judicialRiskData': judicial_risk_data,
            'legalProceedings': legal_proceedings_data,
            'announcement': announcement,
            'weichat': item.weichat,
            'business': business,
            'inveEvent': inveEvent,
            'financing': financing,
            'administrativeLicensing': administrativeLicensing,
            'taxData': taxData,
            'qualificationCertificate': qualificationCertificate,
            'biddingData': biddingData,
            'imExCredit': im_ex_credit,
            'patents': item.patents,
            'xinyongzgs': item.xinyongzgs,
            'trademarkData': trademarkData,
            'copyrightData': copyrightData,
            'worksData': worksData,
            'recordData': recordData,
            'hexin': item.hexin,
            'zuizhongshouyi': item.zuizhongshouyiren,
            'chufa': item.chufa
        }
        data = json.dumps(comp, ensure_ascii=False)
        print(data)
    except Exception as e:
        print(e)

    # print(item.name)




