import time

import pika
import threadpool


def callback(ch, method, properties, body):
    try:
        name = body.decode("utf-8")
        print(name)
        # t = Tianyancah(name)
        # item = t.get_list()
        time.sleep(6)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(e)




def begin(my_task):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='company_name', durable=False)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(callback,
                              queue='company_name',
                              )
        channel.start_consuming()
    except KeyboardInterrupt as e:
        pass


if __name__ == "__main__":
    my_task = [i for i in range(1,3)]
    try:
        pool = threadpool.ThreadPool(3)
        mycorp = threadpool.makeRequests(begin,my_task)
        [pool.putRequest(req) for req in mycorp]
        pool.wait()
    except KeyboardInterrupt as e1:
        pass
    except Exception as e:
        pass







'''docker run -d -p 5672:5672 -p 15672:15672 --name rabbitmq rabbitmq:3.6-management'''