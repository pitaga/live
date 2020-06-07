import sys, os, subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PyQt5.QtGui import *
from PyQt5.QtCore import QObject, pyqtSlot, QUrl
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import ffmpy
import threading


def start_push_stream(ff):
    ff.run()


class Command(QObject):
    # 接收网页发起的信号，执行推流
    @pyqtSlot(str, result=str)
    def executeCommand(self, mess):
        video, audio = self.get_devices()
        self.put_stream(video, audio, mess)
        return mess


    # 获取本机的摄像头、麦克风和屏幕名称
    def get_devices(self):
        cmd = "ffmpeg -list_devices true -f dshow -i dummy"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        lst = str(p.communicate()[1], encoding="utf-8").split("\r\n")
        result = []
        for _ in lst:
            if "dshow" in _ and "Alternative" not in _:
                result.append(_.split(']')[1])
        video = audio = ""
        for i in range(len(result)):
            if "video" in result[i]:
                video = eval(result[i + 1])
            if "audio" in result[i]:
                audio = eval(result[i + 1])
        return video, audio


    # 推流到rtmp服务器
    def put_stream(self, video_name, audio_name, select):
        url = "rtmp://175.24.67.26:1935/live/test"
        fmt = " -pix_fmt yuv420p -c:v libx264 -c:a aac -bf 0 -g 300 -f flv "
        # 多线程推流
        if select == "100":
            threading.Thread(target=start_push_stream, args=(ffmpy.FFmpeg(
                    inputs={"video=" + video_name: "-f dshow -rtbufsize 128M"},
                    outputs={url: fmt}
                ), 
            )).start()
        elif select == "010":
            threading.Thread(target=start_push_stream, args=(ffmpy.FFmpeg(
                    inputs={"audio=" + audio_name: "-f dshow -rtbufsize 128M"},
                    outputs={url: fmt}
                ),
            )).start()
        elif select == "001":
            threading.Thread(target=start_push_stream, args=(ffmpy.FFmpeg(
                    inputs={"desktop": "-f gdigrab -framerate 15"},
                    outputs={url: fmt}
                ),
            )).start()
        elif select == "110":
            threading.Thread(target=start_push_stream, args=(ffmpy.FFmpeg(
                    inputs={
                        "video=" + video_name: "-f dshow -rtbufsize 128M",
                        "audio=" + audio_name: "-f dshow -rtbufsize 128M"
                    },
                    outputs={url: fmt}
                ),
            )).start()
        elif select == "011":
            threading.Thread(target=start_push_stream, args=(ffmpy.FFmpeg(
                    inputs={
                        "desktop": "-f gdigrab -framerate 15",
                        "audio=" + audio_name: "-f dshow -rtbufsize 128M"
                    },
                    outputs={url: fmt}
                ),
            )).start()



if __name__=='__main__':
    # 支援flash
    argvs = sys.argv
    argvs.append('--ppapi-flash-path=./pepflashplayer.dll')
    app = QApplication(argvs)
    
    # 窗口设置
    mainwin = QMainWindow()
    mainwin.resize(1400, 800)

    # 内嵌browser设置
    browser = QWebEngineView()
    browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
    browser.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
    browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)

    # 与前端建立channel通信
    channel = QWebChannel()  # 增加一个通信中需要用到的频道
    commander = Command()   # 通信过程中需要使用到的功能类
    channel.registerObject('commander', commander)  # 将功能类注册到频道中，注册名可以任意，但将在网页中作为标识
    
    # 浏览器设置channel，载入url
    browser.page().setWebChannel(channel)
    browser.load(QUrl('http://192.168.31.166:9999/'))

    # 显示窗口
    mainwin.setCentralWidget(browser)
    mainwin.show()
    sys.exit(app.exec_())