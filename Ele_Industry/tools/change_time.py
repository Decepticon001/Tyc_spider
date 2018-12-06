import re
def GetTime(str):
    time1 = None
    if str is not None:
        a = re.findall(r'\d+-\d+-\d+ \d+:\d+:\d+',str)
        b = re.findall(r'\d+-\d+-\d+',str)
        if a != []:
            time1 = a[0]+'.000'
        if a == []:
            if b!= []:
                time1 = b[0] + ' 00:00:00.000'
    return time1

