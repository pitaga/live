'''
    协程实现异步
'''
import time
import threading


# 写一个关于reqA的装饰器，用于执行原有功能，并添加一些独有的功能
def genCoroutine(func):
    def wrapper(*args, **kwargs):
        gen1 = func()                   # 返回reqA的生成器
        gen2 = next(gen1)               # 返回longIo的生成器
        def run(g):
            res = next(g)
            try:
                gen1.send(res)
            except StopIteration as e:
                pass
        threading.Thread(target=run,args=(gen2,)).start()
    return wrapper


# handler获取数据（数据库、其他服务器、循环耗时）
def longIo():
    print("开始耗时操作")
    time.sleep(5)
    print("开始耗时操作")
    yield "sunck is a good man"         # 返回数据


# 客户A发出的请求
@genCoroutine
def reqA():
    print("开始处理请求A")
    res = yield longIo()                # res接收到longIo发送回的消息时被唤醒继续执行
    print("接收到的数据位", res)
    print("结束处理请求A")


# 客户B发出的请求
def reqB():
    print("开始处理请求B")
    time.sleep(2)
    print("结束处理请求B")


# 模拟tornado服务
def main():
    reqA()                              # 装饰器修饰后的reqA
    reqB()
    while 1:
        time.sleep(0.1)
        pass


if __name__ == "__main__":
    main()