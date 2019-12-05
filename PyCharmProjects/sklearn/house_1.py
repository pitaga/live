###导入模块
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model


###加载训练数据，建立回归方程
datasets_x = []
datasets_y = []
fr = open('prices.txt', 'r')
lines = fr.readlines()
for line in lines:
    items = line.strip().split(',')
    datasets_x.append(int(items[0]))
    datasets_y.append(int(items[1]))
length = len(datasets_x)                                #求得datasets_x的长度，即为数据的总数
datasets_x = np.array(datasets_x).reshape([length, 1])  #将datasets_x转化为数组，并转化为二维
datasets_y = np.array(datasets_y)                       #将datasets_y转化为数组

minX = min(datasets_x)                                  #以数据datasets_x的最大值和最小值为范围，
maxX = max(datasets_x)                                  #建立等差数列，方便后续画图
X = np.arange(minX, maxX).reshape([-1, 1])

linear = linear_model.LinearRegression()                #调用线性回归模块，建立回归方程，拟合函数
linear.fit(datasets_x, datasets_y)

print("Coefficients:{}".format(linear.coef_))
print("intercept:{0:6.2f}".format(linear.intercept_))


###可视化展示
plt.scatter(datasets_x, datasets_y, color="red")        #绘制散点图
plt.plot(X, linear.predict(X), color="blue")            #绘制回归方程
plt.xlabel('Area')
plt.ylabel('Price')
plt.show()