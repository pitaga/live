'''
    接收application的路由，同时处理相应请求
'''
import pymysql
import tornado.web
from tornado.websocket import WebSocketHandler


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("login.html")


class LoginHandler(WebSocketHandler):
    def open(self):
        print("open")
    def on_close(self):
        print("close")
    def on_message(self, message):
        print("on_message")
        print(message)
        lst = message.split(',')
        username, password = lst[0], lst[1]
        status_code = self.is_exist(username, password)
        self.write_message(str(status_code))
    def check_origin(self, origin):
        return True
    def is_exist(self, username, password):
        db = pymysql.connect("localhost", "root", "123456", "chat_room", charset='utf8')
        cursor = db.cursor()
        search_sentence = "select *from user where username='" + username + "'"
        cursor.execute(search_sentence)
        data = cursor.fetchone()
        db.close()
        if data != None:
            if data[1] == password:
                return 200
            else:
                return 500
        else:
            return 404



class SignUpHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("signup.html")
    def post(self, *args, **kwargs):
        username = self.get_body_argument("username")
        password = self.get_body_argument("password")
        password_confirm = self.get_body_argument("password_confirm")
        if password == password_confirm:
            self.addToSQL(username, password)
            self.redirect("/login")
        else:
            self.write("两次输入密码不一致！")
    def addToSQL(self, username, password):
        db = pymysql.connect("localhost", "root", "123456", "chat_room", charset='utf8')
        cursor = db.cursor()
        base_sentence = "insert user (username, password) value"
        sentence = base_sentence + "(" + username + "," + str(password) + ")"
        cursor.execute(sentence)
        db.close()



class HomeHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("chat.html")


class ChatHandler(WebSocketHandler):
    def open(self):
        pass
    def on_message(self, message):
        pass
    def on_close(self):
        pass
    def check_origin(self, origin):
        return True