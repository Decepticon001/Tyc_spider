import datetime

import requests
from lxml import etree
from pandas.core.frame import DataFrame



headers = {
            'Host': 'www.tianyancha.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
            'Cache-Control': 'max-age=0',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            # 'Referer': 'https://www.tianyancha.com/',
            # 'Referer': 'https://www.baidu.com/link?url=aaadddda',
            'Referer':'https://www.baidu.com/link?url=YLvTSuGhlTTvDeRvaJRxwcaZoZfouCq406ty7U_pGKfk9s9Q3iZlqgRhBnchaodzuBpwSzl47wKgPW1jicIoNa&wd=&eqid=e989465400038d08000000065b8f2dd8',
            'Cache-Control': 'max-age=0',
        }

cookies = {'TYCID': '6cf27140b4d211e8957513e011ebbde4', ' undefined': '6cf27140b4d211e8957513e011ebbde4', ' ssuid': '3108248350', ' _ga': 'GA1.2.1978558396.1536567652', ' _gid': 'GA1.2.469262823.1536567652', ' jsid': 'SEM-BAIDU-CG-SY-002185', ' aliyungf_tc': 'AQAAAHlrgHSfkwEAmjr2OrkJizKrr/C1', ' csrfToken': 'RclJTuLH-hDNp-v5uCev8H3i', ' RTYCID': '1f807cebe8c84417852578a48e1eaaf0', ' CT_TYCID': '7b12f570b12b4d1fa01f07cc125d500c', ' token': 'b0ee08121dd444e09de9c32eee77b98a', ' _utm': 'fc20404fa89946949798e9500fa5ba09', ' Hm_lvt_e92c8d65d92d534b0fc290df538b4758': '1536818902,1536823826,1536823990,1536824085', ' tyc-user-info': '%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODAxNzc0MTE3MCIsImlhdCI6MTUzNjgyNDcxNSwiZXhwIjoxNTUyMzc2NzE1fQ.WROAxDhzt1rocM4C5GAZP3-c5N8t1UpiIbhN5ImuLaITPeEjzCXH3WiI7tB-Rd6UV4_LckiRKTTBczNszeayuQ%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%25224%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218017741170%2522%257D', ' auth_token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODAxNzc0MTE3MCIsImlhdCI6MTUzNjgyNDcxNSwiZXhwIjoxNTUyMzc2NzE1fQ.WROAxDhzt1rocM4C5GAZP3-c5N8t1UpiIbhN5ImuLaITPeEjzCXH3WiI7tB-Rd6UV4_LckiRKTTBczNszeayuQ', ' cloud_token': 'd190a77346f0470681aa921a40af9e68', ' Hm_lpvt_e92c8d65d92d534b0fc290df538b4758': '1536824755'}

session = requests.session()
session.headers = headers
requests.utils.add_dict_to_cookiejar(session.cookies, cookies)
with open('../1.html','r',encoding='utf-8') as f:
    html = f.read()

selector = etree.HTML(html)

biangengqian = selector.xpath('//*[@id="_container_changeinfo"]/table/tbody/tr/td[4]/div')
biangengqian_li = []
for i in biangengqian:
    i2 = i.xpath("string(.)")
    biangengqian_li.append(i2)
# print(biangengqian_li)
biangenghou = selector.xpath('//*[@id="_container_changeinfo"]/table/tbody/tr/td[5]/div')
biangenghou_li = []
for r in biangenghou:
    r2 = r.xpath("string(.)")
    biangenghou_li.append(r2)
# print(biangenghou_li)

change_data = DataFrame()
try:
    change_tm = selector.xpath('//*[@id="_container_changeinfo"]/table/tbody/tr/td[2]/text()')
    change_project = selector.xpath('//*[@id="_container_changeinfo"]/table/tbody/tr/td[3]/text()')
    change_be = biangengqian_li
    change_af = biangenghou_li
    # print(len(change_tm),len(change_project),len(change_be),len(change_af))
    change = {
        'change_tm': change_tm,
        'change_project': change_project,
        'change_be': change_be,
        'change_af': change_af
    }
    change_data = DataFrame(change)

except Exception as e:
    print(e)
    pass
# print(change_data)
# print(change_project)
for row in change_data.iterrows():
    change_project = row[1].change_project
    # print(change_project)


Judicial_risk_data = DataFrame()
try:
    hold_court_tm = selector.xpath('//*[@id="_container_announcementcourt"]/table/tbody/tr/td[2]/text()')
    Case = selector.xpath('//*[@id="_container_announcementcourt"]/table/tbody/tr/td[3]/span/text()')
    person = selector.xpath('//*[@id="_container_announcementcourt"]/table/tbody/tr/td[4]/div')
    per = []
    for i in person:
        r = i.xpath('string(.)')
        per.append(r)
    # print(per)
    beigaoren = selector.xpath('//*[@id="_container_announcementcourt"]/table/tbody/tr/td[5]')
    bgr = []
    for i in beigaoren:
        r = i.xpath('string(.)')
        bgr.append(r)
    # print(len(hold_court_tm),len(Case),len(per),len(beigaoren))
    Judicial_risk = {
        'hold_court_tm': hold_court_tm,
        'Case': Case,
        'person': per,
        'bgr': bgr
    }
    Judicial_risk_data = DataFrame(Judicial_risk)
except:
    pass


legal_proceedings_data = DataFrame()
try:
    tm = selector.xpath('//*[@id="_container_lawsuit"]/table/tbody/tr/td[2]/span/text()')
    documents = selector.xpath('//*[@id="_container_lawsuit"]/table/tbody/tr/td[3]/a/text()')
    case = selector.xpath('//*[@id="_container_lawsuit"]/table/tbody/tr/td[4]/span/text()')
    Case_identity = selector.xpath('//*[@id="_container_lawsuit"]/table/tbody/tr/td[5]/div')
    ci = []
    for i in Case_identity:
        r = i.xpath('string(.)')
        ci.append(r)
    case_num = selector.xpath('//*[@id="_container_lawsuit"]/table/tbody/tr/td[6]/span/text()')
    # print(ci)
    legal_proceedings = {
        'tm': tm,
        'documents': documents,
        'case': case,
        'ci' : ci,
        'case_num':case_num
    }
    legal_proceedings_data = DataFrame(legal_proceedings)
except:
    pass
# print(legal_proceedings_data)

announcement_data=DataFrame()
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
    announcement = {
        'tm':tm,
        'ssf':ssf,
        'bsf':bsf,
        'beigaoleixing':beigaoleixing,
        'court':court
    }
    announcement_data = DataFrame(announcement)
except:
    pass
# print(announcement_data)

# Business_data = DataFrame()
# try:
#     business_name = selector.xpath('//*[@id="_container_firmProduct"]/div/a[@class="product"]/div[@class="content"]/div[@class="title"]/text()')
#     type = selector.xpath('//*[@id="_container_firmProduct"]/div/a/div[2]/div[@class="tag tag-new-category"]/text()')
#     desc = selector.xpath('//*[@id="_container_firmProduct"]/div/a/div[2]/div[@class="desc"]/text()')
#     busin_url = selector.xpath('//*[@id="_container_firmProduct"]/div/a[@class="product"]/@onclick')
#     bus_keywords = []
#     bus_des = []
#     reg_tm = []
#     Territoriality = []
#     for u in busin_url:
#         l = u[10:-2].split(",")[0][1:-1]
#         url = "https://www.tianyancha.com/brand/%s"%(l)
#         res1 = session.get(url).text
#         se = etree.HTML(res1)
#         keywords = se.xpath('//div[@class="tags"]/a/text()')
#         keywords = str(keywords)[1:-1].replace("'",'')
#         bus_keywords.append(keywords)
#         reg_time = se.xpath('//span[@class="info"]/text()')[0].split('：')[1]
#         reg_tm.append(reg_time)
#         ter = se.xpath('//span[@class="info"]/text()')[1].split('：')[1]
#         Territoriality.append(ter)
#         des = se.xpath('//*[@id="_container_desc"]/text()')[0]
#         bus_des.append(des)
#     business = {
#         'business_name':business_name,
#         'type':type,
#         'desc':desc,
#         'bus_keywords':bus_keywords,
#         'bus_des':bus_des,
#         'reg_tm':reg_tm,
#         'Territoriality':Territoriality
#     }
#     Business_data = DataFrame(business)
# except:
#     pass

# print(Business_data)

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
    inve_event = {
        'tm':tm,
        'lunci':lunci,
        'jine':jine,
        'touzifang':touzifang,
        'tzf':tzf,
        'product':product,
        'diqu':diqu,
        'ins':ins,
        'busi':busi,
    }
    inve_event_data = DataFrame(inve_event)
except:
    pass


Financing_data = DataFrame()
try:
    tm = selector.xpath('//*[@id="_container_rongzi"]/table/tbody/tr/td[2]/text()')
    rotation = selector.xpath('//*[@id="_container_rongzi"]/table/tbody/tr/td[3]/text()')
    valuation = selector.xpath('//*[@id="_container_rongzi"]/table/tbody/tr/td[4]/text()')
    Amount_of_money = selector.xpath('//*[@id="_container_rongzi"]/table/tbody/tr/td[5]/text()')
    bili = selector.xpath('//*[@id="_container_rongzi"]/table/tbody/tr/td[6]/text()')
    Investor = selector.xpath('//*[@id="_container_rongzi"]/table/tbody/tr/td[7]')
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
        'rotation':rotation,
        'valuation':valuation,
        'Amount_of_money':Amount_of_money,
        'bili':bili,
        'Investors':Investors,
        'newslys':newslys
    }
    Financing_data = DataFrame(Financing)
except:
    pass


administrative_licensing_data = DataFrame()
try:
    xukebianhao = selector.xpath('//*[@id="_container_licensing"]/table/tbody/tr/td[2]/text()')
    xukename = selector.xpath('//*[@id="_container_licensing"]/table/tbody/tr/td[3]/text()')
    youxiaoqizi = selector.xpath('//*[@id="_container_licensing"]/table/tbody/tr/td[4]/text()')
    youxiaoqizhi = selector.xpath('//*[@id="_container_licensing"]/table/tbody/tr/td[5]/text()')
    xukejiguan = selector.xpath('//*[@id="_container_licensing"]/table/tbody/tr/td[6]/text()')
    xukeneirong = selector.xpath('//*[@id="_container_licensing"]/table/tbody/tr/td[7]/text()')
    administrative_licensing = {
        'xukebianhao':xukebianhao,
        'xukename':xukename,
        'youxiaoqizi':youxiaoqizi,
        'youxiaoqizhi':youxiaoqizhi,
        'xukejiguan':xukejiguan,
        'xukeneirong':xukeneirong,
    }
    administrative_licensing_data = DataFrame(administrative_licensing)
except:
    pass
# print(administrative_licensing_data)
# col = administrative_licensing_data.iloc[:,2]
# print(col.values)

Tax_data = DataFrame()
try:
    tm = selector.xpath('//*[@id="_container_taxcredit"]/table/tbody/tr/td[2]/text()')
    tax_rating = selector.xpath('//*[@id="_container_taxcredit"]/table/tbody/tr/td[3]/text()')
    type = selector.xpath('//*[@id="_container_taxcredit"]/table/tbody/tr/td[4]/text()')
    Taxpayer_id = selector.xpath('//*[@id="_container_taxcredit"]/table/tbody/tr/td[5]/text()')
    evaluation_unit = selector.xpath('//*[@id="_container_taxcredit"]/table/tbody/tr/td[6]/text()')
    tax = {
        'tm':tm,
        'tax_rating':tax_rating,
        'type':type,
        'Taxpayer_id':Taxpayer_id,
        'evaluation_unit':evaluation_unit
    }
    Tax_data = DataFrame(tax)
except:
    pass
# print(Tax_data)
Qualification_certificate = DataFrame()
try:
    certificate = selector.xpath('//*[@id="_container_certificate"]/table/tbody/tr/td[2]/span/text()')
    certificate_id = selector.xpath('//*[@id="_container_certificate"]/table/tbody/tr/td[3]/span/text()')
    fazhengriqi = selector.xpath('//*[@id="_container_certificate"]/table/tbody/tr/td[4]/span/text()')
    jiezhiriqi = selector.xpath('//*[@id="_container_certificate"]/table/tbody/tr/td[5]/span/text()')
    Qualification = {
        'certificate':certificate,
        'certificate_id':certificate_id,
        'fazhengriqi':fazhengriqi,
        'jiezhiriqi':jiezhiriqi
    }
    Qualification_certificate = DataFrame(Qualification)
except:
    pass

Bidding_data = DataFrame()
try:
    tm = selector.xpath('//*[@id="_container_bid"]/table/tbody/tr/td[2]/text()')
    title = selector.xpath('//*[@id="_container_bid"]/table/tbody/tr/td[3]/a/text()')
    person = selector.xpath('//*[@id="_container_bid"]/table/tbody/tr/td[4]/text()')
    Bidding = {
        'tm':tm,
        'title':title,
        'person':person
    }
    Bidding_data = DataFrame(Bidding)
except:
    pass


im_ex_credit = DataFrame()
try:
    haiguan = selector.xpath('//*[@id="_container_importAndExport"]/table/tbody/tr/td[1]/text()')
    haiguanbianma = selector.xpath('//*[@id="_container_importAndExport"]/table/tbody/tr/td[2]/text()')
    type = selector.xpath('//*[@id="_container_importAndExport"]/table/tbody/tr/td[3]/text()')
    im_ex = {
        'haiguan':haiguan,
        'haiguanbianma':haiguanbianma,
        'type':type
    }
    im_ex_credit = DataFrame(im_ex)
except:
    pass


Trademark_data = DataFrame()
try:
    reg_tm = selector.xpath('//*[@id="_container_tmInfo"]/div[2]/table/tbody/tr/td[2]/span/text()')
    name = selector.xpath('//*[@id="_container_tmInfo"]/div[2]/table/tbody/tr/td[4]/span/text()')
    reg_id = selector.xpath('//*[@id="_container_tmInfo"]/div[2]/table/tbody/tr/td[5]/span/text()')
    type = selector.xpath('//*[@id="_container_tmInfo"]/div[2]/table/tbody/tr/td[6]/span/text()')
    process_state = selector.xpath('//*[@id="_container_tmInfo"]/div[2]/table/tbody/tr/td[7]/span/text()')
    Trademark = {
        'reg_tm':reg_tm,
        'name':name,
        'reg_id':reg_id,
        'type':type,
        'process_state':process_state
    }
    Trademark_data = DataFrame(Trademark)
except:
    pass

Copyright_data = DataFrame()
try:
    tm = selector.xpath('//*[@id="_container_copyright"]/table/tbody/tr/td[2]/span/text()')
    name = selector.xpath('//*[@id="_container_copyright"]/table/tbody/tr/td[3]/span/text()')
    abbreviation = selector.xpath('//*[@id="_container_copyright"]/table/tbody/tr/td[4]/span/text()')
    register = selector.xpath('//*[@id="_container_copyright"]/table/tbody/tr/td[5]/span/text()')
    type_id = selector.xpath('//*[@id="_container_copyright"]/table/tbody/tr/td[6]/span/text()')
    version = selector.xpath('//*[@id="_container_copyright"]/table/tbody/tr/td[7]/span/text()')
    copyright = {
        'tm':tm,
        'name':name,
        'abbreviation':abbreviation,
        'register':register,
        'type_id':type_id,
        'version':version
    }
    Copyright_data = DataFrame(copyright)
except:
    pass



works_data = DataFrame()
try:
    works_name = selector.xpath('//*[@id="_container_copyrightWorks"]/table/tbody/tr/td[2]/span/text()')
    reg_id = selector.xpath('//*[@id="_container_copyrightWorks"]/table/tbody/tr/td[3]/span/text()')
    type = selector.xpath('//*[@id="_container_copyrightWorks"]/table/tbody/tr/td[4]/span/text()')
    complete_date = selector.xpath('//*[@id="_container_copyrightWorks"]/table/tbody/tr/td[5]/span/text()')
    red_date = selector.xpath('//*[@id="_container_copyrightWorks"]/table/tbody/tr/td[6]/span/text()')
    first_date = selector.xpath('//*[@id="_container_copyrightWorks"]/table/tbody/tr/td[7]/span/text()')
    works = {
        'works_name':works_name,
        'reg_id':reg_id,
        'type':type,
        'complete_date':complete_date,
        'red_date':red_date,
        'first_date':first_date
    }
    works_data = DataFrame(works)
except:
    pass


Record_data = DataFrame()
try:
    examine_tm = selector.xpath('//*[@id="_container_icp"]/table/tbody/tr/td[2]/span/text()')
    website_name = selector.xpath('//*[@id="_container_icp"]/table/tbody/tr/td[3]/span/text()')
    host_page = selector.xpath('//*[@id="_container_icp"]/table/tbody/tr/td[4]/a/@href')
    domain_name = selector.xpath('//*[@id="_container_icp"]/table/tbody/tr/td[5]/text()')
    record = selector.xpath('//*[@id="_container_icp"]/table/tbody/tr/td[6]/span/text()')
    status = selector.xpath('//*[@id="_container_icp"]/table/tbody/tr/td[7]/span/text()')
    nature = selector.xpath('//*[@id="_container_icp"]/table/tbody/tr/td[8]/span/text()')
    record_d = {
        'examine_tm':examine_tm,
        'website_name':website_name,
        'host_page':host_page,
        'domain_name':domain_name,
        'record':record,
        'status':status,
        'nature':nature
    }
    Record_data = DataFrame(record_d)
except:
    pass
print(Record_data)
print(Record_data.loc[0].website_name)
print(Record_data.shape[0])

