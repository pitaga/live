# _*_coding:utf-8_*_
import pika
import serial.tools.list_ports
import re


parameters = pika.URLParameters('amqp://test:123456@192.168.148.51')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='balance')


port_list = list(serial.tools.list_ports.comports())
ser = serial.Serial(port_list[0][0], 9600, timeout=0.5)


cnt_one = 0                 # 定义全局变量计数器，用于函数调用次数的计数
cnt_two = 0
cnt_thr = 0


# serial procession
def process_serial(dire):
    global cnt_one          # 全局变量声明
    global cnt_two
    global cnt_thr
    if dire == 'up':        # 每次up，舵机向上转动5度
        cnt_one -= 1
        ser.write(("servo:1," + str(cnt_one * 5)).encode())
    elif dire == 'down':    # 每次down，舵机向下转动5度
        cnt_one += 1
        ser.write(("servo:1," + str(cnt_one * 5)).encode())
    elif dire == 'left':    # 每次left，舵机向左转动5度
        cnt_two += 1
        ser.write(("servo:2," + str(cnt_two * 5)).encode())
    elif dire == 'right':   # 每次right，舵机向右转动5度
        cnt_two -= 1
        ser.write(("servo:2," + str(cnt_two * 5)).encode())
    elif dire == 'forward': # 每次forward，舵机向前转动5度
        cnt_thr += 1
        ser.write(("servo:3," + str(cnt_thr * 5)).encode())
    elif dire == 'back':    # 每次back，舵机向后转动5度
        cnt_thr -= 1
        ser.write(("servo:3," + str(cnt_thr * 5)).encode())
    elif dire == 'on':        # 写入控制继电器闭合的信号量
        ser.write(("relay:" + dire).encode())
        return
    elif dire == 'off':     # 写入控制继电器关闭的信号量
        ser.write(("relay:" + dire).encode())
        return
    else:                   # 其他情况，直接返回
        print('write message failed')
        return


# the function to receive the message from RabbitMQ
def conversion(mess):
    data = mess.decode('utf-8')
    str_temp = re.findall(r'(?<=dir).*(?=dur)', data)[0]
    direction = re.findall(r'[a-zA-Z]+', str_temp)[0]
    process_serial(direction)


# the function to consume the message
def callback(ch, method, properties, body):
    conversion(body)
    print(body)


# begin consuming the message from the queue 'balance'
channel.basic_consume(callback, queue='balance', no_ack=True)

print(' [*] Waiting for messages.')
channel.start_consuming()