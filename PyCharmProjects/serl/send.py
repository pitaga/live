import serial

ser = serial.Serial("COM6", 9600, timeout=0.5)     #连接串口

mes = input()
while (mes != 'x'):
    ser.write(mes.encode())
    mes = input()