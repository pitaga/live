'''
    用于添加路由，将网址路由到handlers，继承自tornado.web中的Application类
'''

import tornado.web
import config
from views import index


class application(tornado.web.Application):
    # 重写application中的__init__函数
    def __init__(self):
        handlers = [
            (r'/', index.LoginHandler),
            (r'/audience', index.AudienceHandler),
            (r'/anchor', index.AnchorHandler),
            (r'/chat', index.ChatHandler),
            (r'/canvas', index.CanvasHandler),
        ]
        super(application, self).__init__(handlers, **config.settings)