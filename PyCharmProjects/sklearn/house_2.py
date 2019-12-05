###建立工程并导入sklearn包
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures


###加载训练数据，建立回归方程
datasets_x = []                                 #创建两个列表存放房价和面积
datasets_y = []
fr = open('prices.txt', 'r')
lines = fr.readlines()
for line in lines:                              #逐行读取文件中数据
    items = line.strip().split(',')
    datasets_x.append(int(items[0]))
    datasets_y.append(int(items[1]))
length = len(datasets_x)
datasets_x = np.array(datasets_x).reshape(length, 1)
datasets_y = np.array(datasets_y)

minX = min(datasets_x)                          #建立等差矩阵
maxX = max(datasets_x)
X = np.arange(minX, maxX).reshape([-1, 1])

ploy_reg = PolynomialFeatures(degree=2)         #degree=2表示二次多项式
X_ploy = ploy_reg.fit_transform(datasets_x)     #创建二次多项式特征
lin_reg_2 = linear_model.LinearRegression()     #创建线性回归方程
lin_reg_2.fit(X_ploy, datasets_y)               #使用线性模型学习X_poly和datasets_y之间的映射关系


###可视化处理
plt.scatter(datasets_x, datasets_y, color='red')
plt.plot(X, lin_reg_2.predict(ploy_reg.fit_transform(X)), color='blue')
plt.xlabel('Area')
plt.ylabel('Price')
plt.show()