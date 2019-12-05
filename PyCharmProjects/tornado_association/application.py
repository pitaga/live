'''
    用于添加路由，将网址路由到handlers，继承自tornado.web中的Application类
'''

import tornado.web
import os
from tornado_association import config
from tornado_association.views import index


class application(tornado.web.Application):
    # 重写application中的__init__函数
    def __init__(self):
        handlers = [
            (r'/students', index.StudentsHandler),                          # 回调函数异步
            (r'/association', index.AssociationHandler),                    # 协程实现异步
            (r'/final', index.FinalHandler),                                # 最终版本tornado异步请求
            (r'/home', index.HomeHandler),
            # StaticFileHandler放在所有路由的下面，直接调用tornado内部路由
            (r'/(.*)$', tornado.web.StaticFileHandler, {
                "path": os.path.join(config.BASE_DIR, "static/html"),
                "default_filename": "index.html",
            })
        ]
        super(application, self).__init__(handlers, **config.settings)