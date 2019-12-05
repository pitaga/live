import tkinter as tk
from tkinter import messagebox
from tkinter import *
import pika
import serial.tools.list_ports
import re


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = self.master
        self.pack()

        self.link = tk.Button(self, text="连接RabbitMQ", command=self.input)
        self.link.pack(side="left")

        self.quit = tk.Button(self, text="退出", command=self.master.destroy)
        self.quit.pack(side="top", expand=10)

    def input(self):
        win = win_init(400, 240)
        win.title("连接属性")
        Label(win, text="username").place(x=50, y=10, anchor='nw')
        username = Entry(win, bd=1)
        username.place(x=150, y=10, anchor='nw')

        Label(win, text="password").place(x=50, y=50, anchor='nw')
        password = Entry(win, bd=1)
        password.place(x=150, y=50, anchor='nw')

        Label(win, text="ip_address").place(x=50, y=90, anchor='nw')
        ip_address = Entry(win, bd=1)
        ip_address.place(x=150, y=90, anchor='nw')

        Label(win, text="queue_name").place(x=50, y=130, anchor='nw')
        queue = Entry(win, bd=1)
        queue.place(x=150, y=130, anchor='nw')

        clear = tk.Button(win, text="重新输入")
        clear.place(x=100, y=180, anchor='nw')
        clear["command"] = self.clearup(username, password, ip_address, queue)

        commit = tk.Button(win, text="完成输入")
        commit.place(x=220, y=180, anchor='nw')
        commit["command"]=self.commitup(username, password, ip_address, queue)


    def clearup(self, username, password, ip_address, queue):
        username.delete(0, END)
        password.delete(0, END)
        ip_address.delete(0, END)
        queue.delete(0, END)

    def commitup(self, username, password, ip_address, queue):
        print(username.get())


    def link(self, username="test", password="12345", ip_address="0.0.0.0", queue="balance"):
        url = "amqp://" + username + ":" + password + "@" + ip_address
        parameters = pika.URLParameters(url=url)                # 解析amqp链接
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue=queue)
        except:
            messagebox.showinfo("ERROE", "连接RabbitMQ失败，请检查用户名、密码及ip地址！")
            return


def win_init(width, height):
    win = tk.Tk()
    win.resizable(0, 0)                                     # 设置主窗口大小不可更改
    screen_width = win.winfo_screenwidth()                  # 获取当前屏幕分辨率
    screen_height = win.winfo_screenheight()
    x = (screen_width - width) / 2                          # 设置主窗体的偏移量
    y = (screen_height - height) / 2
    win.geometry("%dx%d+%d+%d" % (width, height, x, y))     # 设置窗口大小和窗体偏移量
    return win



if __name__ == "__main__":
    root = win_init(1000, 600)
    app = Application(master=root)
    app.mainloop()