'''
    接收application的路由，同时处理相应请求
'''

import tornado.web

import os
from tornado_exercise import config


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        url = self.reverse_url("kaige")     # 找到name值为kaige的路由，然后反向解析url
        self.write("<a href=%s>去另一个页面</a>"%(url))


class RedirectHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):         # 重定向
        self.redirect('/')


class JsonHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):         # 返回json
        json = {
            "name": "kaige",
            "age": 18,
            "height": 175,
            "weight": 65
        }
        self.write(json)


class HeaderHandler(tornado.web.RequestHandler):
    def set_default_headers(self):          # 设置默认头
        self.set_header("content-type", "text/html; charset=utf-8")
        self.set_header("kaige", "nice")
    def get(self, *args, **kwargs):
        self.set_header("kaige", "good")    # 会覆盖set_default_headers中设置的同名header
        self.write("googd nice")


class StatusCodeHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.set_status(999, "one face mengbi")
        self.write("test success")


class ErrorHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            code = 500
            self.write("服务器错误")
        elif status_code == 404:
            code = 404
            self.write("资源不存在")
        else:
            code = 999
            self.write("one face mengbi")
        self.set_status(code)
    def get(self, *args, **kwargs):
        flag = int(self.get_query_argument("flag"))     # 接收?flag=后的参数
        if flag == 0:
            self.send_error(500)
        elif flag == 2:
            self.send_error(404)
        elif flag == 3:
            self.send_error(123)
        self.write("you are write")


class SunckHandler(tornado.web.RequestHandler):
    def initialize(self, word, *args, **kwargs):
        self.word = word                    # 服务器传递的参数
    def get(self, *args, **kwargs):
        self.write(self.word)


class KaigeHandler(tornado.web.RequestHandler):
    def initialize(self, word, *args, **kwargs):
        self.word = word
    def get(self, *args, **kwargs):
        self.write(self.word)


class LiuHandler(tornado.web.RequestHandler):
    def get(self, p1, p2, p3, *args, **kwargs):
        output = p1 + "-" + p2 + "-" + p3
        print(output)
        self.write("liu is a nice man")


class PostFileHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('postfile.html')
    def post(self, *args, **kwargs):
        first_reward = self.get_body_argument("first_reward")
        second_reward = self.get_body_argument("second_reward")
        third_reward = self.get_body_argument("third_reward")
        print(first_reward, second_reward, third_reward)
        self.write("congratulations! your information has been leaked!")


class AttributeHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        print(self.request.method)      # http请求的方式
        print(self.request.host)        # 被请求的主机
        print(self.request.uri)         # 请求的完整资源地址，包括路径和get查询参数部分
        print(self.request.path)        # 请求路径
        print(self.request.query)       # 请求参数
        print(self.request.version)     # 使用的http版本
        print(self.request.headers)     # 请求协议头，字典类型
        print(self.request.body)        # 请求体数据
        print(self.request.remote_ip)   # 客户机ip地址
        print(self.request.files)       # 用户上传的文件，字典类型
        self.write("print attributions finished")


class UpFileHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("upfile.html")
    def post(self, *args, **kwargs):
        file_dict = self.request.files
        for file_type in file_dict:
            file_arry = file_dict[file_type]
            for file in file_arry:
                file_path = os.path.join(config.BASE_DIR, 'upfile/'+file.filename)      # 文件保存路径
                with open(file_path, "wb") as f:
                    f.write(file.body)
        self.write("up file completed")


class WriteHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("test for buffer memory")
        self.write("test for buffer memory")
        self.finish()       # finish用于刷新缓存区，并关闭当次请求通道。缓存区在换行时会自动清除。
        self.write("test for buffer memory")    # 当次请求的通道已经关闭，本次写入无效。


class HomeHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        person = {
            "name": "very driver",
            "age": 18,
        }
        students = [
            {
                "name": "hapi",
                "age": 18,
            },
            {
                "name": "sunck",
                "age": 21,
            }
        ]
        self.render("home.html", num=10, person=person, students=students)


class FunctionHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        def summary(num1, num2):
            return num1 + num2
        self.render("function.html", fucntion=summary)


class TransformHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        str = "<h1>sunck is a good man</h1>"
        self.render("transform.html", str=str)


class CartHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("cart.html", title="cart")
















