# -*-coding:utf-8-*-
import hashlib


def getFileMD5(filepath):
    f = open(filepath,'rb')
    # a = f.readlines()
    # print(a)
    md5obj = hashlib.md5()
    md5obj.update(f.read())
    hash = md5obj.hexdigest()
    f.close()
    return str(hash).upper()


if __name__ == "__main__":
    md = getFileMD5('/Users/pengzhishen/Downloads/tyc-num.woff')
    print(md)

"""5FA12E3E3CA2E75699246F36A488798C
    12B0DD2605DB0175BC599F9CC182B58B
    991A85169464806602A68C750E0DD4F2
"""
""" https://static.tianyancha.com/fonts-styles/fonts/3b/3b214b0e/tyc-num.woff
    https://static.tianyancha.com/fonts-styles/fonts/5a/5a6b7e77/tyc-num.woff
    """