import time

import redis
import requests

while True:
    try:
        response = requests.get("http://mvip.piping.mogumiao.com/proxy/api/get_ip_bs?appKey=70cf967e9dac4de0a490cddc5540a2c6&count=50&expiryDate=0&format=2&newLine=3").text
        # print(response)

        with open('ips.txt','w',encoding="utf-8") as f:
            f.write(response)
        time.sleep(10)
    except:
        pass