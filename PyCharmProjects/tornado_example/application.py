'''
    用于添加路由，将网址路由到handlers，继承自tornado.web中的Application类
'''

import tornado.web
from tornado_example import config
from tornado_example.views import index


class application(tornado.web.Application):
    # 重写application中的__init__函数
    def __init__(self):
        handlers = [
            (r'/home', index.HomeHandler),
            (r'/chat', index.ChatHandler),
        ]
        super(application, self).__init__(handlers, **config.settings)