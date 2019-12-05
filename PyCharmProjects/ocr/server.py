'''
    主函数，先初始化一个application，用于接收路由，创建一个服务器并绑定端口，开启io循环
'''

import tornado.ioloop
import tornado.httpserver

from ocr import config                      # 导入配置文件
from ocr import application                 # 导入application


if __name__ == "__main__":
    app = application.application()                     # 创建一个app用例，路由到IndexHandler
    httpServer = tornado.httpserver.HTTPServer(app)     # 用app初始化一个httpserver用例
    httpServer.bind(config.options["port"])             # 绑定端口号
    httpServer.start(1)                                 # 开启一个进程
    tornado.ioloop.IOLoop.current().start()             # 开启io循环，监听绑定的端口号
