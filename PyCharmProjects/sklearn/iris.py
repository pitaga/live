import matplotlib.pyplot as plt
#用于实现图形可视化
from sklearn.decomposition import PCA
#加载PCA算法包
from sklearn.datasets import load_iris
#加载鸢尾花数据集导入函数



data = load_iris()                  #使用字典形式获取鸢尾花数据集
x = data.data                       #x表示鸢尾花数据集中的数据属性
y = data.target                     #y表示鸢尾花数据集中的标签
pca = PCA(n_components=2)           #加载PCA算法，设置降维后主成分数目为2
reduced_x = pca.fit_transform(x)    #将降维后的数据保存在reduce_x中


red_x, red_y = [], []       #第一类数据点
blue_x, blue_y = [], []     #第二类数据点
green_x, green_y = [], []   #第三类数据点


#按照鸢尾花的类别将降维后的鸢尾花保存
for i in range(len(reduced_x)):
    if y[i] == 0:
        red_x.append(reduced_x[i][0])
        red_y.append(reduced_x[i][1])
    elif y[i] == 1:
        blue_x.append(reduced_x[i][0])
        blue_y.append(reduced_x[i][1])
    else:
        green_x.append(reduced_x[i][0])
        green_y.append(reduced_x[i][1])


plt.scatter(red_x, red_y, c='r', marker='x')        #第一类数据点
plt.scatter(blue_x, blue_y, c='b', marker='D')      #第二类数据点
plt.scatter(green_x, green_y, c='g', marker='.')    #第三类数据点
plt.show()                                          #可视化