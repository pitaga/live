import serial


cnt_one = 0                 #定义全局变量计数器，用于函数调用次数的计数
cnt_two = 0
cnt_thr = 0

def conversion(sel, dire):
    ser = serial.Serial(sel, 9600, timeout=0.5)     #连接串口
    global cnt_one          #全局变量声明
    global cnt_two
    global cnt_thr
    flag = -1               #舵机的编号
    if dire == b'up':       #每次up，舵机向上转动5度
        flag = 1
        cnt_one += 1
    elif dire == b'down':   #每次down，舵机向下转动5度
        flag = 1
        cnt_one -= 1
    elif dire == b'left':   #每次left，舵机向左转动5度
        flag = 2
        cnt_two += 1
    elif dire == b'right':  #每次right，舵机向右转动5度
        flag = 2
        cnt_two -= 1
    elif dire == b'forward':#每次forward，舵机向前转动5度
        flag = 3
        cnt_thr += 1
    elif dire == b'back':   #每次back，舵机向后转动5度
        flag = 3
        cnt_thr -= 1
    elif dire == b'on':     #写入控制继电器闭合的信号量
        ser.write('on'.encode())
        ser.close()
        return
    elif dire == b'off':    #写入控制继电器关闭的信号量
        ser.write('off'.encode())
        ser.close()
        return
    else:                   #其他情况，直接返回
        ser.close()
        return
    ser.write((str(flag) + ":" + str(cnt_one * 5)).encode())
    ser.write((str(flag) + ":" + str(cnt_two * 5)).encode())
    ser.write((str(flag) + ":" + str(cnt_thr * 5)).encode())
    ser.close()