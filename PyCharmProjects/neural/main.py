import numpy as np
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.core import Flatten, Dense, Dropout
from keras.preprocessing import sequence

# 全局变量
batch_size = 128
epochs = 5
mlen = 300

# 读文件函数
def read_file(filepath):
    x_file = open(filepath)
    lst = x_file.read().splitlines()
    result = []
    for str in lst:
        a = str[1:len(str)-1].split(',')
        temp = list(map(int, a))
        result.append(temp)
    return sequence.pad_sequences(result, maxlen=mlen)

# 载入训练数据
X_train = read_file("../neural/train_data/x.txt")
Y_train = np.loadtxt("../neural/train_data/y.txt").astype(int)
X_test = read_file("../neural/train_data/xx.txt")
Y_test = np.loadtxt("../neural/train_data/yy.txt").astype(int)


# 构建模型
model = Sequential()

# 嵌入层
model.add(Dense(50, activation="relu", input_dim=mlen))

# 隐藏 layer
model.add(Dropout(0.3, noise_shape=None, seed=None))
model.add(Dense(15, activation="relu"))
model.add(Dropout(0.2, noise_shape=None, seed=None))
model.add(Dense(15, activation="relu"))

# 输出层
model.add(Dense(1, activation="sigmoid"))

# 编译模型
model.compile(loss = "binary_crossentropy",         # 分类的loss函数
              optimizer = "adam",                   # 优化器
              metrics = ["accuracy"])

# 训练模型
result = model.fit(X_train, Y_train, batch_size=batch_size,
                   epochs=epochs, validation_data=(X_test, Y_test))

# 评估训练模型
score, acc = model.evaluate(X_test, Y_test, batch_size=batch_size)
print('Test score:', score)
print('Test accuracy:', acc)