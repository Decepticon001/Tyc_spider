# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 09:54:08 2018

@author: spz
"""

# -*-coding:utf-8-*-
import datetime
import json

import redis
import stomp
import time
import threadpool

from tianyanchaspider.get_tianyancha import Tianyancah


r = redis.Redis(host='localhost',port=6379, db=0)
queue_name = 'com.huihan.qilian.companies'
# queue_name = 'com.huihan.qilian.test'
listener_name = 'MyListener'
post = 61613
conn = stomp.Connection10([('47.105.121.234', post)])
conn.start()
conn.connect()






class MyListener(object):
    def on_error(self, headers, message):
        print('received an error %s' % message)
    def on_message(self, headers, message):
        print('received a message %s' % message)



def get_message(my_task):

    while True:
        item = ''
        company_name = r.brpop("company_name", 0)[1].decode("utf-8")
        company_name = company_name.replace(r"\xa0", "")
        try:
            print(company_name)
            if company_name.startswith("#") or company_name.startswith("$"):
                company_name = company_name[1:]
            # company_name = "百度（中国）有限公司"
            t = Tianyancah(company_name)
            item = t.get_list()
        except Exception as e:
            print(e)
            r.rpush("company_name", company_name)
        if item == '':
            continue
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
                # 'logo':item.logo,
                'corpCode': item.tongyixinyongdaima,
                'organizingInstitutionBarCode': item.zuzhijigoudaima,
                'industryAndCommerce': item.gongshangzhuce,
                'identificationNumberOfTheTaxpayer': item.nashuirenshibiehao,
                'operatingPeriod': item.regtm,
                'checkAndApprove': item.hezhunriqi,
                'registrationAuthority': item.dengjijiguan,
                'registeredAssets': item.zhuceziben,
                'jystatus': item.jystatus,
                'renyuanguimo':item.renyuanguimo,
                'EnglishName':item.yingwenming,
                'nashuirenzizhi':item.nashuirenzizhi,
                'shijiaoziben':item.shijiaoziben,
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
                'hexin':item.hexin,
                'zuizhongshouyi':item.zuizhongshouyiren,
                'chufa':item.chufa
            }
            data = json.dumps(comp, ensure_ascii=False)
        except Exception as e:
            print(e)
        # print(data)
        try:
            # with open("data.txt","a+") as f:
            #     f.write("%s\n"%data)
            conn.send(queue_name, data)
            print(data)
            # with open("data.txt","a+") as f:
            #     f.write("%s\n"%(data))
            print("保存成功")
            time.sleep(5)
        except Exception as e:
            print(e)




if __name__ == "__main__":
    my_task = [i for i in range(1)]
    try:
        pool = threadpool.ThreadPool(1)
        mycorp = threadpool.makeRequests(get_message,my_task)
        [pool.putRequest(req) for req in mycorp]
        pool.wait()
    except Exception as e:
        pass
    finally:
        conn.disconnect()

'''10.52'''

"""6861979 15.56 """ '''17.16 825232 [55669  46511]'''
'''中南红文化集团股份有限公司

哈尔滨博实自动化股份有限公司
'the label [13] is not in the [index]'

江苏凤凰出版传媒股份有限公司

长春奥普光电技术股份有限公司
'the label [6] is not in the [index]'

暴风集团股份有限公司
'''