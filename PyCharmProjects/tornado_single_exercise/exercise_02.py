import tornado.web
import tornado.ioloop
import tornado.httpserver

from project import config                              # 导入自定义配置文件


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("just for a test")                   # 向网页中写入just for a test


if __name__ == "__main__":
    # 创建一个app用例，路由到IndexHandler
    app = tornado.web.Application([
        (r'/', IndexHandler)
    ])

    # 以下代码等同于app.listen(port)
    httpServer = tornado.httpserver.HTTPServer(app)     # 用app初始化一个httpserver用例
    httpServer.bind(config.options["port"])             # 绑定端口号
    httpServer.start(1)                                 # 开启一个进程

    # 开启io循环，监听绑定的端口号
    tornado.ioloop.IOLoop.current().start()
