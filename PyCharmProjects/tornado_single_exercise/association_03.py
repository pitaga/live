'''
    协程实现异步
'''
import time
import threading

gen = None


# handler获取数据（数据库、其他服务器、循环耗时）
def longIo():
    def run():
        print("开始耗时操作")
        time.sleep(5)
        try:
            global gen
            gen.send("sunck is a good man")         # 信息send到  res=yeild longIo()  这一行
        except StopIteration as e:
            pass
        threading.Thread(target=run).start()
        print("结束耗时操作")


# 写一个关于reqA的装饰器，用于执行原有功能，并添加一些独有的功能
def genCoroutine(func):
    def wrapper(*args, **kwargs):
        global gen
        gen = func(*args, **kwargs)
        next(gen)
    return wrapper


# 客户A发出的请求
@genCoroutine
def reqA():
    print("开始处理请求A")
    res = yield longIo()        # res接收到longIo发送回的消息时被唤醒继续执行
    print("接收到的数据位", res)
    print("结束处理请求A")


# 客户B发出的请求
def reqB():
    print("开始处理请求B")
    time.sleep(2)
    print("结束处理请求B")


# 模拟tornado服务
def main():
    reqA()                      # 装饰器修饰后的reqA
    reqB()
    while 1:
        time.sleep(0.1)
        pass


if __name__ == "__main__":
    main()