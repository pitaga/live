'''
    接收application的路由，同时处理相应请求
'''

import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient
import json


class StaticFileHanlder(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(StaticFileHanlder, self).__init__(*args, **kwargs)
        self.xsrf_token


class StudentsHandler(tornado.web.RequestHandler):
    def on_response(self, response):
        if response.error:
            self.send_error(500)
        else:
            data = json.loads(response.body)
            self.write(data)
        self.finish()                   # 手动关闭通信通道

    @tornado.gen.coroutine              # get调用完成后，不关闭通信通道，实现长链接
    def get(self, *args, **kwargs):
        url = "https://news.sina.com.cn/roll/"
        # 创建客户端
        client = AsyncHTTPClient()
        client.fetch(url, callback=self.on_response)
        self.write("finished")


class AssociationHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        url = "https://news.sina.com.cn/roll/"
        client = AsyncHTTPClient()
        res = yield client.fetch(url)   # 协程的实现
        if res.error:
            self.send_error(500)
        else:
            data = json.loads(res.body)
            self.write(data)


class FinalHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        res = yield self.getData()
        self.write(res)
    # 耗时操作
    @tornado.gen.coroutine
    def getData(self):
        url = "https://news.sina.com.cn/roll/"
        client = AsyncHTTPClient()
        res = yield client.fetch(url)
        if res.error:
            ret = {"ret": 0}
        else:
            ret = json.loads(res.body)
        raise tornado.gen.Return(ret)   # 相当于send


class HomeHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("home")