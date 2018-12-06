import requests

res = requests.get("https://img.tianyancha.com/logo/lll/9c72f6a6b37b4dcf2ece8f31a3237ec2.png@!f_200x200").content
print(res)