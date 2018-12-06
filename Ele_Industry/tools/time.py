
import time
import random
def Get_Time():
    a1=(2018,3,23,0,0,0,0,0,0)              #设置开始日期时间元组（1976-01-01 00：00：00）
    a2=(2018,3,23,23,59,59,0,0,0)    #设置结束日期时间元组（1990-12-31 23：59：59）
    start=time.mktime(a1)    #生成开始时间戳
    end=time.mktime(a2)
    t = random.randrange(start,end)
    local_time = time.localtime(t)
    data_head = time.strftime("%H:%M:%S", local_time)
    time_stamp = "%s.%s" % (data_head, str(t)[-3:])
    return time_stamp
# print(Get_Time())
def get_data_time():
    time1 = time.ctime()
    str_time = 'GMT+0800 (中国标准时间)'
    list1 = time1.split(' ')
    a = list1[3]
    list1[3] = list1[4]
    list1[4] = a
    data_time = ' '.join(list1) + ' ' + str_time
    return data_time
