import ffmpy
import subprocess, sys, os


# 获取本机的摄像头、麦克风和屏幕名称
def get_devices():
    cmd = "ffmpeg -list_devices true -f dshow -i dummy"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    lst = str(p.communicate()[1], encoding="utf-8").split("\r\n")
    # 根据关键字筛选设备名
    result = []
    for _ in lst:
        if "dshow" in _ and "Alternative" not in _:
            result.append(_.split(']')[1])
    # 获取设备名
    video = audio = ""
    for i in range(len(result)):
        if "video" in result[i]:
            video = '"' + eval(result[i + 1]) + '"'
        if "audio" in result[i]:
            audio = '"' + eval(result[i + 1]) + '"'
    return video, audio


def put_stream(video_name, audio_name, select):
    url = "rtmp://175.24.67.26:1935/live/test"
    fmt = " -pix_fmt yuv420p -c:v libx264 -c:a aac -bf 0 -g 300 -f flv "

    video = "ffmpeg -f dshow -rtbufsize 128M -i video=" + video_name + fmt + url
    audio = "ffmpeg -f dshow -rtbufsize 128M -i audio=" + audio_name + fmt + url
    screen = "ffmpeg -f gdigrab -framerate 15 -i desktop" + fmt + url
    video_audio = "ffmpeg -f dshow -rtbufsize 128M -i video=" + video_name + \
                  " -f dshow -rtbufsize 128M -i audio=" + audio_name + fmt + url
    screen_audio = "ffmpeg -f gdigrab -framerate 15 -i desktop" + \
                   " -f dshow -rtbufsize 128M -i audio=" + audio_name + fmt + url

    if select == "100":
        p = subprocess.Popen(video, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    elif select == "010":
        p = subprocess.Popen(audio, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    elif select == "001":
        p = subprocess.Popen(screen, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    elif select == "110":
        p = subprocess.Popen(video_audio, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen(screen_audio, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    print("select = ", select, "\n", str(p.communicate()[1], encoding="utf-8"))
