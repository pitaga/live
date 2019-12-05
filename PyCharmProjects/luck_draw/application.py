import tornado.web

from luck_draw import config
from luck_draw.view import index


class application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', index.IndexHandler),
            (r'/homepage', index.HomePageHandler),
        ]
        super(application, self).__init__(handlers, **config.settings)