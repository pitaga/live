import tornado.web
import numpy as np


class IndexHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("content-type", "text/html; charset=utf-8")
    def get(self, *args, **kwargs):
        self.redirect("/homepage")


class HomePageHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("homepage.html")
    def post(self, *args, **kwargs):
        data = self.get_body_arguments("award")             # 获取设定的中奖人数
        file = self.request.files["name_list"][0]           # 获取中奖名单

        first, second, third = self.process_message(data, file)
        self.display(first, "一等奖")
        self.display(second, "二等奖")
        self.display(third, "三等奖")

    def process_message(self, Data, File):
        try:                                                # 解析上传的文本文档
            name_list = File.body.decode("UTF-8").split("、")
        except:
            name_list = File.body.decode("ISO-8859-1").split("、")

        number = list(map(int, Data))                       # 解析用户设置的各等奖的数量
        sum = number[0] + number[1] + number[2]             # 获取设置的中奖总数和各等将对应的index
        start = number[0]
        middle = number[0] + number[1]

        if sum > len(name_list):                            # 若设置的中奖人数大于参与人员，向参与人员名单中添加“无人中奖”
            for _ in range(sum - len(name_list)):
                name_list.append("无人中奖")

        name_arry = np.array(name_list)                     # 一次性抽奖
        result = np.random.choice(name_arry, sum, replace=False)
        return result[:start], result[start:middle], result[middle:]    # 获取抽奖结果

    def display(self, arry, num_str):
        lst = list(set(arry.tolist()))
        if "无人中奖" in lst and len(lst)>1:
            lst.remove("无人中奖")
        self.write("<center><h3>" + num_str + "</h3>")
        count = 1
        for item in lst:
            self.write(item + "\t")
            count = count + 1
            if count%10 == 0:
                self.write("<br>")
        self.write("</table></center>")