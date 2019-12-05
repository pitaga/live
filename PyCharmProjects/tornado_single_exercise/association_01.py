'''
    callbaack回调函数实现异步
'''
import time
import threading


# handler获取数据（数据库、其他服务器、循环耗时）
def longIo(callback):
    def run(cb):
        print("开始耗时操作")
        time.sleep(5)
        print("结束耗时操作")
        cb("sunck is a good man")
    threading.Thread(target=run, args=(callback,)).start()


# 函数（回调函数）
def finish(data):
    print("开始处理回调函数")
    print("接收到longIo的响应数据:", data)
    print("结束处理回调函数")


# 客户A的请求
def reqA():
    print("开始处理reqA")
    longIo(finish)
    print("结束处理reqB")


# 客户B的请求
def reqB():
    print("开始处理reqB")
    time.sleep(2)
    print("结束处理reqB")


# tornado服务
def main():
    reqA()
    reqB()
    while 1:
        time.sleep(0.1)
        pass
