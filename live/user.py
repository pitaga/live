# 维护一个用户类，用于存放用户的username,password,chat_log

class User():
    def __init__(self, username, password, select): # 用username和password初始化一个实例
        self.username = username
        self.password = password
        self.identify = select

    def get_username(self):                         # 返回当前用户名
        return self.username

    def get_password(self):                         # 返回当前用户密码
        return self.password

    def get_identify(self):
        return self.identify

    def get_uid(self):                              # 获取uid
        return self.uid

    def set_uid(self, user):                        # 设定uid
        self.uid = user

