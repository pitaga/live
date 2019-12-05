# 维护一个用户类，用于存放用户的username,password,chat_log

class User():
    def __init__(self, username, password):         # 用username和password初始化一个实例
        self.username = username
        self.password = password
        self.chat_log = []

    def get_username(self):                         # 返回当前用户名
        return self.username

    def get_password(self):                         # 返回当前用户密码
        return self.password

    def get_uid(self):                              # 获取uid
        return self.uid

    def set_uid(self, user):                        # 设定uid
        self.uid = user

    def get_chat_log(self, chat_room):              # 返回特定聊天室当前用户的聊天记录
        result = []
        for item in self.chat_log:
            if chat_room == item["name"]:
                result = item["message"]
        return result

    def add_chat_log(self, username, chat_room, message):     # 当前用户当前聊天室添加聊天记录
        flag = False
        for item in self.chat_log:
            if chat_room == item["name"]:
                mess = "[" + username + "]:" + message
                item["message"].append(mess)
                flag = True
        if flag == False:
            log = {
                "name": chat_room,
                "message": [],
            }
            mess = "[" + username + "]:" + message
            log["message"].append(mess)
            self.chat_log.append(log)
