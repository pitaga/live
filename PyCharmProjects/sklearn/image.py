import numpy as np
import PIL.Image as image
#加载PIL包，用于加载图片
from sklearn.cluster import KMeans
#加载KMeans算法



def loadData(filePath):
    f = open(filePath, 'rb')        #以二进制形式打开文件
    data = []
    img = image.open(f)             #以列表形式返回图片像素值
    m, n = img.size                 #获得图片的大小
    for i in range(m):              #将每个像素点RGB颜色处理到0-1的范围
        for j in range(n):
            x, y, z = img.getpixel((i, j))
            data.append([x/256.0, z/256.0])
    f.close()
    return np.mat(data), m, n       #以矩阵形式返回data，以及图片大小

imgData, row, col = loadData('original.jpg')     #加载数据


km = KMeans(n_clusters=3)           #聚类中心个数为3


#聚类获得每个像素所属的类别
label = km.fit_predict(imgData)
label = label.reshape([row, col])
#创建一张新的灰度图保存聚类后的结果
pic_new = image.new("L", (row, col))
#根据所属类向图片中添加灰度值
for i in range(row):
    for j in range(col):
        pic_new.putpixel((i, j), int(256/(label[i][j]+1)))
        #使用pillow4.x版本需要将像素值转化为int型
#以JPEG格式保存图片
pic_new.save("result.jpg", "JPEG")