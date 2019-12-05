import pymysql

username = "username"
password = "password"

db = pymysql.connect("localhost", "root", "123456", "chat_room", charset='utf8')
cursor = db.cursor()
base_sentence = "insert user (username, password) value"
sentence = base_sentence + "('" + username + "','" + password + "')"
cursor.execute(sentence)
db.commit()
cursor.close()
db.close()