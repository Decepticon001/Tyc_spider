import time
import asyncio
from aiohttp import ClientSession, TCPConnector, BasicAuth
from lxml import etree



async def fetch(url, session):
    proxy_auth = BasicAuth('HUIHANHTTTEST1', 'LDJUC95z')
    headers = {'connection': 'closed'}
    async with session.get(url=url,
                           proxy="http://http-proxy-sg1.dobel.cn:9180",
                           proxy_auth=proxy_auth,
                           headers=headers) as resp:
        ss = await resp.read()
        s = ss.decode("utf-8")
        # print(s)
        selector = etree.HTML(s)
        u = selector.xpath("/html/body/div[3]/div[1]/div[5]/div/div[2]/div[3]/a/@href")
        print(u)
        # return await resp.read()


connector = TCPConnector(limit=60)
session = ClientSession(connector=connector)
nums = 100
# url = 'https://www.taobao.com/help/getip.php'
url = "http://shuidi.cn/b-search?key=腾讯科技（深圳）有限公司"

tasks = [fetch(url, session) for x in range(nums)]
try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
except:
        pass
finally:
        loop.close()
        session.close()
