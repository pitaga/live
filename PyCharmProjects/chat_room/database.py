# 数据库查询和写入操作
import pymysql

class DataBase():
    # 初始化一个database对象
    def __init__(self, username, password):
        self.username = username
        self.password = password
    # 链接数据库，查询用户名是否已经存在
    def is_exist_database(self):
        db = pymysql.connect("localhost", "root", "123456", "chat_room", charset='utf8')
        cursor = db.cursor()
        search_sentence = "select *from user where username='" + self.username + "'"
        cursor.execute(search_sentence)
        data = cursor.fetchone()
        cursor.close()
        db.close()
        return data
    # 将用户名和密码加入数据库
    def addToSQL(self):
        db = pymysql.connect("localhost", "root", "123456", "chat_room", charset='utf8')
        cursor = db.cursor()
        base_sentence = "insert user (username, password) value"
        sentence = base_sentence + "('" + self.username + "','" + self.password + "')"
        cursor.execute(sentence)
        db.commit()
        cursor.close()
        db.close()