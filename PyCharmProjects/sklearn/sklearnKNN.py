###1）建立工程并导入sklearn包
import numpy as np
from os import listdir
from sklearn import neighbors





###2）加载训练数据
def img2vector(filename):
    retMat = np.zeros([1024], int)          #定义返回矩阵，大小为1*1024
    fr = open(filename)                     #打开包含32*32大小的数字文件
    lines = fr.readlines()                  #读取文件的所有行
    for i in range(32):                     #遍历文件所有行
        for j in range(32):                 #并将0/1数字存放在retMat中
            retMat[i*32+j] = lines[i][j]
    return retMat

def readDataSet(path):
    fileList = listdir(path)                #获取文件夹下的所有文件
    numFiles = len(fileList)                #统计需要读取的文件的数目
    dataSet = np.zeros([numFiles,1024], int)#用于存放所有的数字文件
    hwLabels = np.zeros([numFiles])         #用于存放对应的标签（与神经网络不同）
    for i in range(numFiles):               #遍历所有文件
        filePath = fileList[i]              #获取文件名称/路径
        digit = int(filePath.split('_')[0]) #通过文件名获取标签
        hwLabels[i] = digit                 #直接存放数字，并非ont-hot向量
        dataSet[i] = img2vector(path + '/' + filePath)  #读取文件内容
    return dataSet, hwLabels

train_dataSet, train_hwLabels = readDataSet('trainingDigits')





###3）构造KNN分类器
knn = neighbors.KNeighborsClassifier(algorithm='kd_tree', n_neighbors=3)
knn.fit(train_dataSet, train_hwLabels)





###4）测试集评价
test_dataSet, test_hwLabels = readDataSet('testDigits')

res = knn.predict(test_dataSet)                 #对测试集进行预测
error_num = np.sum(res != test_hwLabels)        #统计分类器错误的数目
num = len(test_dataSet)                         #测试集的数目
print("Total num:", num, "\nRight num:", num-error_num,
      "\nRight Rate:", 1-error_num/float(num))