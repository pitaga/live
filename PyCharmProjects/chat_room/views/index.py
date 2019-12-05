'''
    接收application的路由，同时处理相应请求
'''
import tornado.web
from chat_room import database, user
from tornado.websocket import WebSocketHandler

import re
import json

# 全局变量，user实例列表，chat_room实例列表
clients = []
rooms = []


class LoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("login.html")
    def post(self):
        username = self.get_body_argument("username")
        password = self.get_body_argument("password")
        db = database.DataBase(username, password)
        data = db.is_exist_database()
        if data != None:
            if data[1] == password:
                clients.append(user.User(username, password))
                self.redirect("/home")
            else:
                self.write("密码输入错误")
        else:
            self.redirect("/signup")


class SignUpHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("signup.html")
    def post(self, *args, **kwargs):
        message = self.get_argument("message")
        username = re.findall(r'(?<=username=).*(?=&)', message)[0]
        password = re.findall(r'(?<=password=).*', message)[0]
        db = database.DataBase(username, password)
        data = db.is_exist_database()
        if data == None:
            db.addToSQL()
            clients.append(user.User(username, password))
            self.write('success')
        else:
            self.write("用户名已被占用")


class HomeHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("chat.html")
    # ajax动态请求将用户名发送到前端
    def post(self):
        self.write(clients[-1].get_username())


class ChatHandler(WebSocketHandler):
    # 打开网页时将所有用户加入到users
    all_users = []
    def open(self):
        self.all_users.append(self)
    # 向前端发送打包后的json数据
    def on_message(self, data):
        self.bind_uid(data)
        self.send_json(data)
    # 关闭网页时将self对象从所有聊天室的members中去除
    def on_close(self):
        for item in rooms:
            for member in item["members"]:
                if self == member:
                    item["members"].remove(self)
        self.all_users.remove(self)


    # self对象绑定uid
    def bind_uid(self, data):
        data = json.loads(data)
        username = data["username"]
        for item in clients:
            if item.get_username() == username:
                item.set_uid(self)

    # 将待发送消息打包成json发送
    def send_json(self, data):
        data = json.loads(data)
        type = data["type"]
        if type == "button":
            result = self.button(data)
            for user in self.all_users:
                user.write_message(result)
        else:
            users = self.get_room_members(data["chat_room"])
            if type == "enter_room":
                result, chat_log = self.enter_room(data)
                for user in users:
                    user.write_message(result)
                log_mess = {
                    "type": "chat_log",
                    "chat_log": chat_log,
                    "history": "-----------------以上为历史记录-----------------",
                }
                self.write_message(log_mess)
            elif type == "message":
                result = self.message(data)
                for user in users:
                    user.write_message(result)

    # 分类将接收到的消息进行转换成待发送消息
    def enter_room(self, data):
        username = data["username"]
        last_room = data["last_room"]
        chat_room = data["chat_room"]
        content = username + " 进入了 " + chat_room
        # 将self对象从last_room中剔除，加入chat_room
        self.update_member_list(chat_room, last_room)
        # 获取当前用户在此聊天室期间的聊天记录
        chat_log = self.get_chat_log(username, chat_room)
        result = {
            "type": "enter_room",
            "content": content,
        }
        return result, chat_log
    def message(self, data):
        username = data["username"]
        message = data["message"]
        chat_room = data["chat_room"]
        # 将message加入到chat_room的聊天记录列表中
        users = self.get_room_members(chat_room)
        for user in users:
            user.update_chat_log(user, username, chat_room, message)
        content = u"[%s]:%s" % (username, message)
        result = {
            "type": "message",
            "content": content,
        }
        return result
    def button(self, data):
        button = data["button"]
        room_name = data["chat_room"]
        result = {
            "type": "button",
            "button": button,
            "room_name": room_name,
        }
        return result

    # 更新聊天室成员
    def update_member_list(self, chat_room, last_room):
        if chat_room != last_room:
            flag = False
            for item in rooms:
                if item["name"] == last_room:
                    item["members"].remove(self)
                if item["name"] == chat_room:
                    item["members"].append(self)
                    flag = True
            if flag == False:
                room = {
                    "name": chat_room,
                    "members": []
                }
                room["members"].append(self)
                rooms.append(room)
        for item in rooms:
            item["members"] = list(set(item["members"]))

    # 获取room_name聊天室的当前所有成员
    def get_room_members(self, room_name):
        result = []
        for item in rooms:
            if item["name"] == room_name:
                result = item["members"]
        return result

    # 更新username名下在chat_room中的聊天记录
    def update_chat_log(self, user, username, chat_room, message):
        for item in clients:
            if item.get_uid() == user:
                item.add_chat_log(username, chat_room, message)

    # 获取username名下chat_room聊天室中的聊天记录
    def get_chat_log(self, username, chat_room):
        result = []
        for item in clients:
            if item.get_username() == username:
                result = item.get_chat_log(chat_room)
        return result

