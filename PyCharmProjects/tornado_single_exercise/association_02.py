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


# 客户A发出的请求
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
    global gen
    gen = reqA()        # 用协程写的，生成一个生成器
    next(gen)           # 执行reqA，执行到yeild longIo()时被挂起，开始执行reqB

    reqB()
    while 1:
        time.sleep(0.1)
        pass


if __name__ == "__main__":
    main()