###建立工程，并导入sklearn包
import numpy as np          #导入numpy工具包
from os import listdir      #导入listdir模块，用于访问本地文件
from sklearn.neural_network import MLPClassifier    #导入神经网络分类器



###加载训练数据
def img2vector(filename):
    retMat = np.zeros([1024], int)          #定义返回的矩阵，大小为1*1024
    fr = open(filename)                     #打开32*32的数字文件
    lines = fr.readlines()                  #读取文件的所有行
    for i in range(32):                     #遍历文件的所有行，并将文件中的0和1存放到retMat中
        for j in range(32):
            retMat[i*32+j] = lines[i][j]
    return retMat

def readDataSet(path):
    fileList = listdir(path)                    #获取文件夹下的所有文件
    numFiles = len(fileList)                    #统计需要读取的文件的数目
    dataSet = np.zeros([numFiles, 1024], int)   #用于存放所有的数据文件
    hwLabels = np.zeros([numFiles, 10])         #用于存放对应的标签one-hot
    for i in range(numFiles):                   #遍历所有的文件
        filepath = fileList[i]                  #获取文件的名称/路径
        digit = int(filepath.split('_')[0])
        hwLabels[i][digit] = 1.0                #将对应的one-hot标签置1
        dataSet[i] = img2vector(path + '/' + filepath)      #读取文件内容
    return dataSet, hwLabels

train_dataSet, train_hwLabels = readDataSet('trainingDigits')
#在sklearnBP.py中调用readDataSet和img2vector函数来加载数据，
#将训练的图片存放在train_dataSet中，
#对应的标签顺序则存放在train_hwLabels中



###训练神经网络
clf = MLPClassifier(hidden_layer_sizes=(100,),
                    activation='logistic', solver='adam',
                    learning_rate_init=0.0001,
                    max_iter=3675)
#设置100个神经元的隐藏层
#hidden_layer_sizes存放的是一个元祖，并令出事学习率为0.0001

clf.fit(train_dataSet, train_hwLabels)
#fit函数能够根据训练集及对应标签集自动设置多层感知机的输入输出层的神经元个数
#例如train_dataSet为n*1024的矩阵，train_hwLabels为n*1024的矩阵，
#则fit函数将MLP的输入层神经元个数设为1024，输出层神经元个数10.



###测试集评价
dataSet, hwLabels = readDataSet('testDigits')
#在sklearnBP.py中，加载测试集
res = clf.predict(dataSet)          #对测试集进行预测
error_num = 0                       #统计预测错误的数目
num = len(dataSet)                  #测试集的数目
for i in range(num):                #遍历预测结果
    if np.sum(res[i] == hwLabels[i]) < 10:      #若比较长度为10的数组，返回包含01的数组，0为不同，
        error_num += 1                          #1为相同，若预测结果与真是结果相同，则10哥数字全为1
print("Total num:", num, "Wrong num:", error_num, "WrongRate:", error_num/float(num))