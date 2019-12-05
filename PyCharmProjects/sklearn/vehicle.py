###创建工程并导入包
import numpy as np
from sklearn.linear_model import Ridge
#通过sklearn加载岭回归方法
from sklearn.model_selection import train_test_split
#加载交叉验证模块       #*#4.x版本中如以上语句#*#
import matplotlib.pyplot as plt
#加载matplotlib模块
from sklearn.preprocessing import PolynomialFeatures
#通过sklearn加载PolynomialFeatures模块，用于创建多项式特征


###加载数据
data = np.genfromtxt('vehicle.txt')
#使用numpy的方法从txt中加载数据
plt.plot(data[:, 4])
#使用plt展示车流量信息


###数据处理
x = data[:, :4]                     #x用于保存0--3维的数据，即属性
y = data[:, 4]                      #y用于保存4维的数据，即车流量
ploy = PolynomialFeatures(6)        #用于创建最高次数为6次方的多项式特征方程，多次试验后决定采用6次
x = ploy.fit_transform(x)           #x为创建的多项式


###划分训练集和测试集    #*#4.x版本中如以上语句#*#
train_set_x, test_set_x, train_set_y, test_set_y = train_test_split(x, y, test_size=0.3, random_state=0)
#将所有数据划分为训练集和测试集，test_size表示测试集的比例，random_state是随机种子


###创建回归器，并进行训练
clf = Ridge(alpha=1.0, fit_intercept=True)      #创建岭回归实例
clf.fit(train_set_x, train_set_y)               #调用fit函数使用训练集训练回归函数
clf.score(test_set_x, test_set_y)               #利用测试集计算回归曲线的拟合度，clf.score返回值为0.7375
#拟合度，用于评价拟合好坏，最大为1，最小为0，当对所有输入输出都是一个值的时候，拟合度为0。


###绘制拟合曲线
start = 0                       #绘制一段0--9的拟合曲线
end = 9
y_pre = clf.predict(x)          #调用predict函数的拟合值
time = np.arange(start, end)
plt.plot(time, y[start:end], 'b', label="real")         #展示真实数据颜色蓝色
plt.plot(time, y_pre[start:end], 'r', label="predict")  #展示拟合曲线颜色红色
plt.legend(loc="upper left")    #设置拟合曲线位置
plt.show()                      #可视化