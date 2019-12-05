import base64, os, re
from flower_recognition import config
import matplotlib.pyplot as plt


# 完成转码，写入图像，转换图像格式一系列操作
def saveToLocal(data):
    b64code = re.findall(r'(?<=base64,).*', data)[0]
    bytecode = base64.b64decode(b64code)
    filename = os.path.join(config.BASE_DIR, "image/test.png")
    with open(filename, "wb+") as f:
        f.write(bytecode)
    print("predict picture has been saved in ", filename)


# 显示图片在服务器
def display():
    image = plt.imread("image/test.png")
    plt.imshow(image)
    plt.show()
