import numpy as np
from sklearn.naive_bayes import GaussianNB


x = np.array([[-1,-1], [-2,-1], [-3,-2], [1,1], [2,1], [3,2]])
y = np.array([1, 2, 3, 4, 5, 6])

clf = GaussianNB(priors=None)       #使用默认参数构造一个朴素贝叶斯分类器

clf.fit(x, y)                       #fit函数进行训练
a = clf.predict([[1.0, 2.0]])       #predict函数进行预测，返回一个数组

print(a)