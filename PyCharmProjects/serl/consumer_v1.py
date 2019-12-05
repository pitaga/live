import pika
import serial



parameters = pika.URLParameters('amqp://test:123456@192.168.148.51')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='balance')


ser = serial.Serial("COM6", 9600, timeout=0.5)      # 连接串口

cnt_one = 0                 #定义全局变量计数器，用于函数调用次数的计数
cnt_two = 0
cnt_thr = 0
def conversion(sel, dire):
    global cnt_one          #全局变量声明
    global cnt_two
    global cnt_thr
    if dire == b'up':       #每次up，舵机向上转动5度
        cnt_one += 1
        sel.write((str(1) + ":" + str(cnt_one * 5)).encode())
    elif dire == b'down':   #每次down，舵机向下转动5度
        cnt_one -= 1
        sel.write((str(1) + ":" + str(cnt_one * 5)).encode())
    elif dire == b'left':   #每次left，舵机向左转动5度
        cnt_two += 1
        sel.write((str(2) + ":" + str(cnt_two * 5)).encode())
    elif dire == b'right':  #每次right，舵机向右转动5度
        cnt_two -= 1
        sel.write((str(2) + ":" + str(cnt_two * 5)).encode())
    elif dire == b'forward':#每次forward，舵机向前转动5度
        cnt_thr += 1
        sel.write((str(3) + ":" + str(cnt_thr * 5)).encode())
    elif dire == b'back':   #每次back，舵机向后转动5度
        cnt_thr -= 1
        sel.write((str(3) + ":" + str(cnt_thr * 5)).encode())
    elif dire == b'on':     #写入控制继电器闭合的信号量
        sel.write('on'.encode())
        sel.close()
        return
    elif dire == b'off':    #写入控制继电器关闭的信号量
        sel.write('off'.encode())
        sel.close()
        return
    else:                   #其他情况，直接返回
        return


def callback(ch, method, properties, body):
    conversion(ser, body)
    print(body)


channel.basic_consume(callback, queue='balance', no_ack=True)

print(' [*] Waiting for messages.')
channel.start_consuming()