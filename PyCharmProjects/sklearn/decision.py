from sklearn.datasets import load_iris
#导入鸢尾花数据集
from sklearn.tree import DecisionTreeClassifier
#导入决策树分类器
from sklearn.model_selection import cross_val_score
#导入计算交叉验证的函数cross_val_score


clf = DecisionTreeClassifier()
#使用默认参数创建一棵基于基尼系数的决策树
iris = load_iris()
#将鸢尾花数据集赋值给iris

arry = cross_val_score(clf, iris.data, iris.target, cv=10)
#iris.data作为特征，iris.target作为目标结果，cv=10作为交叉验证

print(arry)