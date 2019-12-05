'''
    接收application的路由，同时处理相应请求
'''


import tornado.web
from tornado.websocket import WebSocketHandler
from flower_recognition import predict


from flower_recognition import image


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class HomeHandler(WebSocketHandler):
    def on_message(self, message):
        image.saveToLocal(message)      # 将base64码转化为图片并保存到服务器本地，以便之后的预测
        image.display()                 # 在服务端使用matplotlib显示图片
        result = predict.predict()      # 预测图片，并返回结果
        self.write_message(result)      # 将结果返回给前端
