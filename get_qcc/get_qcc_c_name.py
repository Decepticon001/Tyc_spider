import logging


data = "1111231"
logging.basicConfig(filename='../comp_log/comp.log', level=logging.INFO)
logging.info('%s'%(data))
