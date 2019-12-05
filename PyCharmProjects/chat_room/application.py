'''
    用于添加路由，将网址路由到handlers，继承自tornado.web中的Application类
'''

import tornado.web
from chat_room import config
from chat_room.views import index


class application(tornado.web.Application):
    # 重写application中的__init__函数
    def __init__(self):
        handlers = [
            (r'/', index.LoginHandler),
            (r'/home', index.HomeHandler),
            (r'/signup', index.SignUpHandler),
            (r'/chat', index.ChatHandler),
        ]
        super(application, self).__init__(handlers, **config.settings)