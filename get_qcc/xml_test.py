from xml.dom.minidom import parse
import xml.dom.minidom

from fontTools import unichr

DOMTree = xml.dom.minidom.parse('/Users/pengzhishen/Downloads/tyc-num.ttx')
collection = DOMTree.documentElement

codes = collection.getElementsByTagName("cmap_format_12")[0]
codes1 = codes.getElementsByTagName('map')
# print(codes1)

# print(len(codes1))
for code in codes1:
   if code.hasAttribute("code"):
      # print("%s" % code.getAttribute("code"))
      # print(int(str(code.getAttribute("code")),16))
      ss = int(str(code.getAttribute("code")),16)
      print(unichr(ss))