import pika

parameters = pika.URLParameters('amqp://test:123456@192.168.148.51')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='balance')


channel.basic_publish(exchange='', routing_key='balance', body='up')
connection.close()