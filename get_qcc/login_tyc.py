import  requests
import stomp
from lxml import etree

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'qznewsite.uid=dmkjivumg2vnbsegjozeynx1; Hm_lvt_55ad112b0079dd9ab00429af7113d5e3=1539251259; Hm_lpvt_55ad112b0079dd9ab00429af7113d5e3=1539251323',
    'Host': 'www.qichamao.com',
    'Referer': 'https://www.qichamao.com/search/all/%E8%85%BE%E8%AE%AF?o=0&area=0&mfccode=-9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}

res = requests.get("https://www.qichamao.com/orgcompany/searchitemdtl/09daaa18aa1758d63cee090949263587.html",headers=headers).text
se = etree.HTML(res)
fw = se.xpath('//section[@class="pb-d2"]/ul/li[16]/span[2]/text()')
print(fw)