import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.core import Flatten, Dense, Dropout


# 全局变量
batch_size = 32
bn_classes = 3
epochs = 30

# 构建模型
model = Sequential()
model.add(Embedding(69214, 32, input_length=100))   # 嵌入层
model.add(Flatten())                                # 一维化
model.add(Dense(64, activation="sigmoid"))          # 全链接层
model.add(Dropout(0.5))
model.add(Dense(32, activation="sigmoid"))
model.add(Dropout(0.5))
model.add((Dense(3, activation="softmax")))         # 输出层

# 编译模型
model.compile(loss = "categorical_crossentropy",    # 分类的loss函数
              optimizer = "adadelta",               # 优化器
              metrics = ["accuracy"])

# 训练模型
result = model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs,
                   verbose=1, validation_data=(X_train, Y_train)).history

# 保存模型
model.save("../neural/train_model.h5")