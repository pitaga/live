'''
    用于添加路由，将网址路由到handlers，继承自tornado.web中的Application类
'''

import tornado.web
import os
from tornado_exercise import config
from tornado_exercise.views import index


class application(tornado.web.Application):
    # 重写application中的__init__函数
    def __init__(self):
        handlers = [
            (r'/', index.IndexHandler),                 # 主页
            (r'/index', index.RedirectHandler),         # 重定向
            (r'/header', index.HeaderHandler),          # 响应头
            (r'/json', index.JsonHandler),              # 返回json
            (r'/status', index.StatusCodeHandler),      # 状态码
            (r'/error', index.ErrorHandler),            # 错误处理(error?flag=1)
            (r'/sunck', index.SunckHandler, {"word": "sunck"}),     # 传递参数
            # 反向解析,在不改变链接的情况下可以改变路由,如果使用name属性,不能使用元组,必须使用tornado.web.url()定义路由
            tornado.web.url(r'/kaige', index.KaigeHandler, {"word": "kaige"}, name="kaige"),
            # 服务器接收参数(正则表达式?P<name>表示命名一个name的group)
            (r'/liu/(?P<p2>w+)/(?P<p3>w+)/(?P<p1>w+)', index.LiuHandler),
            (r'/postfile', index.PostFileHandler),      # 返回html模板
            (r'/attribute', index.AttributeHandler),    # 打印request的各个属性
            (r'/upfile', index.UpFileHandler),          # 上传文件
            (r'/write', index.WriteHandler),            # 清除缓存
            (r'/home', index.HomeHandler),              # 渲染网页
            (r'/function', index.FunctionHandler),      # 向网页传递函数
            (r'/transform', index.TransformHandler),    # 转义字符
            (r'/cart', index.CartHandler),              # 继承

            # StaticFileHandler放在所有路由的下面，直接调用tornado内部路由
            (r'/(.*)$', tornado.web.StaticFileHandler, {
                "path": os.path.join(config.BASE_DIR, "static/html"),
                "default_filename": "index.html",
            })
        ]
        super(application, self).__init__(handlers, **config.settings)
