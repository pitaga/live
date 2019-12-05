from keras.layers.core import *
from keras.models import *
import numpy as np

'''共2000个句子'''


class NNsentiment(object):
    def __init__(self, positiveFile, negativeFile, labelFile, batch_size=32, epochs=2, text=None):
        self.positive_review = open(positiveFile, "rb")
        self.negative_review = open(negativeFile, "rb")
        self.label_file = open(labelFile, "r")
        self.vocab = {}  # 词汇表，字典形式
        self.vocab_len = 0  # 词汇表长度
        self.words = []  # 存储所有行源单词数据
        self.word_data = []  # 存储所有行中单词转换为词汇表索引的数据
        self.word_vec = []  # 存储所有行中每个单词的词向量
        self.label_list = []  # 标签列表
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []
        self.batch_size = batch_size
        self.epochs = epochs
        self.model = None  # 存储训练完的神经网络模型
        self.text = text

    def bytes2str(self, data):  # 返回单词列表
        tmp = []
        for c in bytes.decode(data.strip()).split():  # 字节数据转换为字符串数据并按空格分开形成list
            tmp.append(c)
        return tmp

    def createVoc(self):  # 设置self.vocab及self.vocab_len
        self.positive_review.seek(0)  # 设置光标至起始位置
        self.negative_review.seek(0)
        vocab = set()  # 确保无序不重复
        # positive_context
        line1 = self.bytes2str(self.positive_review.readline())
        while line1:
            for i in line1:
                vocab.add(i)  # 添加每行所有出现的单词
            line1 = self.bytes2str(self.positive_review.readline())
        # negative_context
        line2 = self.bytes2str(self.negative_review.readline())
        while line2:
            for i in line2:
                vocab.add(i)
            line2 = self.bytes2str(self.negative_review.readline())
        vocab_list = list(vocab)  # 集合转换为列表
        vocab_dict = dict.fromkeys(vocab_list)  # 将列表转换为字典，单词与索引对应，提高检索效率
        index = 1  # 从1开始
        for k in vocab_dict.keys():   # 设置字典索引
            vocab_dict[k] = index
            index += 1
        self.vocab = vocab_dict
        self.vocab_len = len(self.vocab)  # 获得词汇表长度以设置input_dim

    def createWords(self):  # 设置self.words, self.data
        self.positive_review.seek(0)  # 设置光标至起始位置
        self.negative_review.seek(0)
        # 按label中存放顺序先读取negative
        # negative_context
        line = self.bytes2str(self.negative_review.readline())   # 读取每行内容，每行中单词按空格隔开存入列表
        while line:
            self.words.append(line)
            vec = []
            for word in line:  # vec与line一一对应
                vec.append(self.vocab.get(word))
            self.word_data.append(vec)  # 将一行向量append到self.word_vec
            line = self.bytes2str(self.negative_review.readline())
        self.negative_review.close()
        # positive_context
        line = self.bytes2str(self.positive_review.readline())
        while line:
            self.words.append(line)
            vec = []
            for word in line:  # vec与line一一对应
                vec.append(self.vocab.get(word))
            self.word_data.append(vec)  # 将一行向量append到self.word_vec
            line = self.bytes2str(self.positive_review.readline())
        self.positive_review.close()

    def word2vec(self):
        self.word_vec = np.zeros((len(self.word_data), self.vocab_len+1))  # 词汇表索引从1开始，所以dimension + 1
        for i, data in enumerate(self.word_data):
            self.word_vec[i, data] = 1   # 单词对应词汇表的索引的对应位置置1

    def readLabel(self):  # 设置self.label_list
        self.label_file.seek(0)  # 设置光标至起始位置
        line = self.label_file.readline().strip()
        while line:
            self.label_list.append(int(line))  # 将每行读到的label加到self.label_list
            line = self.label_file.readline().strip()
        self.label_file.close()

    def nn(self):
        model = Sequential()
        model.add(Dense(50, activation="relu", input_dim=self.vocab_len+1))  # 接收np.array, 从1开始索引, dimension = 词汇表长度加1


        # hidden layer
        model.add(Dropout(0.3, noise_shape=None, seed=None))
        model.add(Dense(15, activation="relu"))
        model.add(Dropout(0.2, noise_shape=None, seed=None))
        model.add(Dense(15, activation="relu"))

        # output_layer
        model.add(Dense(1, activation="sigmoid"))

        model.compile(optimizer="adam", loss="mse", metrics=["accuracy"])

        result = model.fit(self.x_train, self.y_train, epochs=self.epochs,
                           batch_size=self.batch_size, validation_data=(self.x_test, self.y_test))
        model.save("sentiment.txt")
        print("Test accuracy: ", np.mean(result.history["val_acc"]))

    def run(self):
        self.createVoc()
        self.createWords()
        self.word2vec()
        self.readLabel()
        print(self.word_vec[0])
        # 训练数据集
        self.x_train = self.word_vec[:880]
        self.x_train = list(self.x_train)
        self.x_train.extend(self.word_vec[1018:1803])
        self.x_train = np.array(self.x_train)
        # 训练标签
        y_train = self.label_list[:880]
        y_train.extend(self.label_list[1018:1803])
        self.y_train = np.array(y_train)
        # 测试数据集
        self.x_test = self.word_vec[880:1018]
        self.x_test = list(self.x_test)
        self.x_test.extend(self.word_vec[1803:])
        self.x_test = np.array(self.x_test)
        # 测试标签
        y_test = self.label_list[880:1018]
        y_test.extend(self.label_list[1803:])
        self.y_test = np.array(y_test)

        self.nn()


def main():
   test = NNsentiment("../neural/train_data/positive.review",
                      "../neural/train_data/negative.review",
                      "../neural/train_data/y.txt", batch_size=32,  epochs=5)
   test.run()


if __name__ == "__main__":
    main()
