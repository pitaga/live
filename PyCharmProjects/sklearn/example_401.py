import numpy as np                                      #导入numpy库和pandas库
import pandas as pd

from sklearn.preprocessing import Imputer               #从sklearn库中导入预处理模块Imputer
from sklearn.model_selection import train_test_split    #导入自动训练集和测试集的模块train_test_split
from sklearn.metrics import classification_report       #导入预测结果评估模块classification_report

from sklearn.neighbors import KNeighborsClassifier      #导入K近邻分类器
from sklearn.tree import DecisionTreeClassifier         #导入决策树分类器
from sklearn.naive_bayes import GaussianNB              #导入高斯朴素贝叶斯函数





def load_dataset(feature_paths, label_paths):
    """读取特征文件列表和标签文件列表中的内容，回归后返回
    """
    feature = np.ndarray(shape=(0, 41))
    #定义feature数组变量，列数量和特征维度一致为41
    label = np.ndarray(shape=(0, 1))
    #定义空的标签变量，列数量和标签维度一致为1

    for file in feature_paths:
        #使用逗号分隔符读取特征数据，将问号替换标记为缺失值，文件不包括表头
        df = pd.read_table(file, delimiter=',', na_values='?', header=None)
        #使用平均值补全缺失值，文件中不包含表头
        imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
        imp.fit(df)
        df = imp.transform(df)
        #将新读入的数据合并到特征集合中
        feature = np.concatenate((feature, df))

    for file in label_paths:
        #读取标签数据，文件不包含表头
        df = pd.read_table(file, header=None)
        #将读入的数据合并到标签集合中
        label = np.concatenate((label, df))
    #将label转化为一位向量
    label = np.ravel(label)

    return feature, label





if __name__ == '__main__':
    #设置数据路径
    feature_paths = ['A/A.feature', 'B/B.feature', 'C/C.feature', 'D/D.feature', 'E/E.feature']
    label_paths = ['A/A.label', 'B/B.label', 'C/C.label', 'D/D.label', 'E/E.label']

    #将前四个数作为训练集读入
    x_train, y_train = load_dataset(feature_paths[:4], label_paths[:4])
    #将最后一个数读入
    x_test, y_test = load_dataset(feature_paths[4:], label_paths[4:])

    #使用全局数据作为训练集，并借助train_test_split函数将训练数据打乱
    x_train, x_, y_train, y_ = train_test_split(x_train, y_train, test_size=0.0)

    #创建K近邻分类器，并在分类器上进行测试
    print("start training knn")
    knn = KNeighborsClassifier().fit(x_train, y_train)
    print("training done")
    answer_knn = knn.predict(x_test)
    print("prediction done")

    #创建决策树分类器并在决策树分类器上进行测试
    print("start training dt")
    dt = DecisionTreeClassifier().fit(x_train, y_train)
    print("training done")
    answer_dt = dt.predict(x_test)
    print("prediction done")

    #创建高斯朴素贝叶斯函数，并惊醒测试
    print("start training bayes")
    gnb = GaussianNB().fit(x_train, y_train)
    print("training done")
    answer_gnb = gnb.predict(x_test)
    print("prediction done")

    #计算准确率及召回率
    print("\n\nThe classification of knn:")
    print(classification_report(y_test, answer_knn))
    print("\n\nThe classification of dt:")
    print(classification_report(y_test, answer_dt))
    print("\n\nThe classification of gnb")
    print(classification_report(y_test, answer_gnb))