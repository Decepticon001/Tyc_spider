# -*- coding: utf-8 -*-
from urllib.parse import urljoin
import re

from bs4 import BeautifulSoup
from lxml import etree
from scrapy import Selector
from lxml import etree
import logging
img_str_link = 'imglink url="{}" imglink'
def change_content(content,xpath,url=None):
    """
    处理内容
    :param content:
    :param xpath:
    :param url:
    :return:
    """
    rule = r'src="(.*?)"'
    img_list = re.compile(rule,re.S).findall(content)
    html_body = content
    # 没有图片不需要处理
    if img_list != []:
        for img_url in img_list:
            img_src = urljoin(url,img_url)
            html_body = html_body.replace(img_url,img_src)
        img_link = re.findall(r'<img.*?>',html_body)
        if img_link != []:
            for img in img_link:
                url = re.findall(r'src="(.*?)"',img)
                if url == []:
                    logging.error(content)
                img_str = img_str_link.format(url[0])
                html_body = html_body.replace(img,img_str)
    from requests_html import HTML
    html1 = HTML(html=html_body)
    # # print(html1.markdown)
    html_body = html1.xpath(xpath)[0].text
    return html_body


# import hashlib
#
# # 待加密信息
# str = '江苏明月光电科技有限公司'
#
# # 创建md5对象
# hl = hashlib.md5()
#
# # Tips
# # 此处必须声明encode
# # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
# hl.update(str.encode(encoding='utf-8'))
# print(hl.hexdigest())
#
#
#
#
# html="""
# <div class="bmsg job_msg inbox">
# 						岗位职责<br>1、销售管理职位，负责其功能领域内主要目标和计划；<br>2、制定、参与或协助上层执行相关的政策和制度；<br>3、负责区域的销售运作，包括计划、组织、进度控制和检讨；<br>4、分析和开发市场并搞好售后服务；<br><br>任职资格<br>1、大专以上学历；<br>2、有做营销的愿望和激情；<br>2、有销售经验或应届大学毕业生均可；<br>3、出色的市场分析洞察能力、具备全面深刻营销知识和技能；<br>4、具备一定的管理领导能力和沟通协调能力；<br>5、江苏省13个地级市驻地区域经理，各城市本地人。
# 												<div class="mt10">
# 														<p class="fp">
# 								<span class="label">职能类别：</span>
# 																	<span class="el">销售代表</span>
# 																</p>
# 																					<p class="fp">
# 								<span class="label">关键字：</span>
# 																	<span class="el">销售营销业务</span>
# 															</p>
# 													</div>
# 						<div class="share">
# 							<a track-type="jobsButtonClick" event-type="6" class="a" href="javascript:void(0);" id="fenxiang">分享</a>
# 							<div class="shareBox">
# 								<div id="weixinMa_fx" style="display:none;"><img width="198" height="198" alt="二维码" src="https://jobs.51job.com/comm/qrcode.php?url=https%3A%2F%2Fm.51job.com%2Fsearch%2Fjobdetail.php%3Fjobid%3D96516324"></div>
# 								<a class="icon_b i_weixin" href="javascript:;" onclick="weixinMa();">微信</a>
# 								<a class="icon_b i_mail" target="_blank" href="http://my.51job.com/sc/sendjob_tofriend.php?jobid=96516324&amp;coid=3511134&amp;divid=0">邮件</a>
# 							</div>
# 						</div>
# 						<div class="clear"></div>
# 					</div>
#
#
# 					"""
# from requests_html import HTML
# html1 = HTML(html=html)
# # # print(html1.markdown)
# html_body = html1.xpath('//div[@class="bmsg job_msg inbox"]')[0].text
# print(html_body)
# # html_body = change_content(html,'//section[@class="textblock"]')
# # with open('1.txt','w',encoding='utf-8') as f:
# #     f.write(html_body)
# # # print(html_body)
# # from requests_html import HTMLSession
# #
# # session = HTMLSession()
# # r = session.get('https://toutiao.hc360.com/2/29822.html')
# # print(r.html.xpath('//div[@class="textblock"]'))
# # print(r.html.decode('utf-8','ignore').find('#textblock'))
# # print(r)
# # print(r.html.xpath('//div[@class="textblock"'))
# # print(r.html.links)
# # from requests_html import session
# # from requests_html import session
# # soup = BeautifulSoup(html_body,'html.parser',from_encoding='utf-8')
# # info = soup.find('div',class_='text_box1 cl')
# # print(soup.text)
# # html_body = etree.HTML(html_body)
# # info = html_body.xpath('//div[@class="text_box1 cl"]')
# # print(info[0])
# # selector = Selector(text=html_body)
# # bloger = selector.xpath('//section [@class="textblock"]')
# # print(bloger.xpath('string(.)').extract_first())
# # bloger = selector.xpath('//div[@class="art-con article_body"]')
# # info = bloger.text
# # print(info)
# # import html2text
# # print (html2text.html2text(html))
#
#
# # print(html1.links)
# # from tomd import Tomd
# # a = Tomd(html_body).markdown
# # # pattern = '[\\\`\*\_\[\]\#\+\-\!\>]'
# # pattern = '[\\\`\*\_\[\]\#\+\-\!\>]'
# # partter1 = '&nbsp;&nbsp;&nbsp;&nbsp;'
# # content_text3 = re.sub(pattern, ' ', a)
# # content_text4 = re.sub(partter1, '  ', content_text3)
# # partter2 = '(http:.*?.com)'
# # content_text5 = re.sub(partter2, '  ', content_text4)
#
# # print(content_text5)
# # print(a)
#
# # sample_text = '''
# #     The textwrap module can be used to format text for output in
# #     situations where pretty-printing is desired.  It offers
# #     programmatic functionality similar to the paragraph wrapping
# #     or filling features found in many text editors.
# # '''
# # import textwrap
# # print(a[0].text)
# # b = textwrap.fill(a[0].text,initial_indent='',subsequent_indent=' ' * 4,)
# #
# # print(b)