'''
    接收application的路由，同时处理相应请求
'''
import tornado.web
from tornado.websocket import WebSocketHandler
import user


# 当前所有用户
current_users = []

# 登录
class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("login.html")
    def post(self):
        username = self.get_body_argument("username")
        password = self.get_body_argument("password")
        select = self.get_body_argument("select")
        current_users.append(user.User(username, password, select))
        if select == 'audience':
            self.redirect('audience')
        elif select == 'anchor':
            self.redirect('anchor')
        # ajax动态请求将用户名发送到前端
        print("当前用户信息：", username, password, select)


# 观众
class AudienceHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("audience.html")
    def post(self):
        self.write(current_users[-1].get_username())


# 主播
class AnchorHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("anchor.html")
    def post(self):
        self.write(current_users[-1].get_username())


# 聊天室
class ChatHandler(WebSocketHandler):
    # 打开网页时将所有用户加入到users
    current_users_object = []
    def open(self):
        self.current_users_object.append(self)

    # 向前端发送打包后的json数据
    def on_message(self, data):
        for _ in self.current_users_object:
            _.write_message(data)

    # 关闭网页时将self从当前用户列表中去除
    def on_close(self):
        self.current_users_object.remove(self)


# 白板演示
class CanvasHandler(tornado.web.RedirectHandler):
    def get(self):
        self.render("canvas.html")
    def post(self):
        pass