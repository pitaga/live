import tornado.ioloop
import tornado.httpserver

from luck_draw import config
from luck_draw import application


if __name__ == "__main__":
    app = application.application()
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.bind(config.options["port"])
    httpServer.start(1)
    tornado.ioloop.IOLoop.current().start()
