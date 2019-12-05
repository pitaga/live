'''
    接收application的路由，同时处理相应请求
'''

import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("just for a test")