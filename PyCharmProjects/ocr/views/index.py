'''
    接收application的路由，同时处理相应请求
'''

import tornado.web
from tornado.websocket import WebSocketHandler

from ocr import image
from ocr import test


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class HomeHandler(WebSocketHandler):
    def open(self):
        self.pred = test.Predict()
    def on_message(self, message):
        test_data = image.ImagePrepare(message).get_image()
        self.output_in_server(test_data)
        result = self.pred.predict(test_data)
        self.write_message(str(result))
    def output_in_server(self, data):
        for i in range(32):
            for j in range(32):
                if data[i][j] != 0:
                    print(data[i][j], end="")
                else:
                    print(" ", end="")
            print()