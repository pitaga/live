import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver


tornado.options.define("port", default=8000, type=int)
tornado.options.define("list", default=[], type=str, multiple=True)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("just for a test")


if __name__ == "__main__":
    # tornado.options.parse_command_line()              # 从命令行转换参数
    # 命令行执行命令 python exercise_01.py  --port=9000  --list=good,hangsome,fine,cool  --logging=None

    # tornado.options.options.logging = None            # 关闭日志
    tornado.options.parse_config_file("config")         # 从配置文件转换参数

    print("list=", tornado.options.options.list)

    # 创建一个app用例，路由到IndexHandler
    app = tornado.web.Application([
        (r'/', IndexHandler)
    ])

    # 以下代码等同于app.listen(port)
    httpServer = tornado.httpserver.HTTPServer(app)     # 用app初始化一个httpserver用例
    httpServer.bind(tornado.options.options.port)       # 绑定端口号
    httpServer.start(1)                                 # 开启一个进程

    # 开启io循环，监听绑定的端口号
    tornado.ioloop.IOLoop.current().start()
