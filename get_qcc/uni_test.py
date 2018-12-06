import random
import time
from multiprocessing import Process
import os
from multiprocessing import Pool

import threadpool

def get_message(task):
    print(1)



def long_time_task(name):
    my_task = [i for i in range(0, 6)]
    try:
        pool = threadpool.ThreadPool(6)
        mycorp = threadpool.makeRequests(get_message, my_task)
        [pool.putRequest(req) for req in mycorp]
        pool.wait()
    except Exception as e:
        pass


if __name__=='__main__':
    p = Pool(4)   # 创建4个进程
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    p.close()
    p.join()


"14.43 	1502136 15.03  "