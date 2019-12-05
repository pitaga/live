'''
    接收application的路由，同时处理相应请求
'''

import tornado.web
from tornado.websocket import WebSocketHandler


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")


class ChatHandler(WebSocketHandler):
    users = []
    def open(self):                             # 进入网页时调用
        self.users.append(self)
        for user in self.users:                 # 遍历当前所有客户机，显示信息给全部客户机
            user.write_message(u"[%s]进入聊天室"%(self.request.remote_ip))

    def on_message(self, message):              # 用于接收从前端发送给服务器的信息
        for user in self.users:
            user.write_message(u"[%s]\n:%s"%(self.request.remote_ip, message))

    def on_close(self):                         # 关闭浏览器网页时调用
        self.users.remove(self)
        for user in self.users:
            user.write_message(u"[%s]退出了聊天室"%(self.request.remote_ip))

    def check_origin(self, origin):
        return True