#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: fuck_tyc_font.py
@time: 2018-09-20 14:02
"""
import os

from PIL import Image, ImageFont, ImageDraw
from xml.dom.minidom import parse
import xml.dom.minidom

from fontTools import unichr

DOMTree = xml.dom.minidom.parse('/Users/pengzhishen/Downloads/tyc-num.ttx')
collection = DOMTree.documentElement

codes = collection.getElementsByTagName("cmap_format_12")[0]
codes1 = codes.getElementsByTagName('map')

for code in codes1:
   if code.hasAttribute("code"):
      ss = int(str(code.getAttribute("code")),16)
      char = unichr(ss)
      text = u'%s' % (char)
      im = Image.new('RGB', (130, 130), (255, 255, 255))
      dr = ImageDraw.Draw(im)
      font = ImageFont.truetype(os.path.join('fonts', '/Users/pengzhishen/Downloads/tyc-num.woff'), 100)
      dr.text((12, 10), text, font=font, fill='#000000')
      # im.show()
      im.save('/Users/pengzhishen/Downloads/image/%s.png' % (char))
      im.close()

# for a in charlist:
#     text = u'%s'%(a)
#     im = Image.new('RGB', (130, 130), (255, 255, 255))
#     dr = ImageDraw.Draw(im)
#     font = ImageFont.truetype(os.path.join('fonts', '/Users/pengzhishen/Downloads/tyc-num.woff'), 100)
#     dr.text((12, 10), text, font=font, fill='#000000')
#     # im.show()
#     im.save('/Users/pengzhishen/Downloads/image/%s.png'%(a))
#     im.close()
