import base64, os, re, cv2
from ocr import config
from PIL import Image


class ImagePrepare():
    # 初始化函数，完成转码，写入图像，转换图像格式一系列操作
    def __init__(self, data):
        self.path = "image/predict.png"
        img_data = self.get_code(data)
        self.saveImage(img_data)
        self.image = self.convertImageToopencv()
    # 转码，base64转化为字节流
    def get_code(self, data):
        pat = r'(?<=base64,).*'
        b64code = re.findall(pat, data)[0]
        result = base64.b64decode(b64code)
        return result
    # 保存图像到服务器本地
    def saveImage(self, img_data):
        filename = os.path.join(config.BASE_DIR, self.path)
        with open(filename, "wb") as f:
            f.write(img_data)
    # PIL.Image格式转为OpenCV格式，便于进行缩放和锐化等操作
    def convertImageToopencv(self):
        image = Image.open("image/predict.png")
        result = cv2.imread("image/predict.png", 0)
        height, width = image.size
        for i in range(height):
            for j in range(width):
                result[j][i] = int(image.getpixel((i, j))[-1])
        dst = cv2.resize(result, (32, 32), interpolation=cv2.INTER_AREA)    # INTER_AREA插值
        dst_x = cv2.Sobel(dst, -1, 1, 0)    # 索贝尔锐化
        dst_y = cv2.Sobel(dst, -1, 0, 1)
        dst = cv2.add(dst_x, dst_y)
        return dst
    # 返回OpenCV格式的图像
    def get_image(self):
        return self.image
