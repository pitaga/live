import os
import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from tensorflow.contrib.layers import flatten
from sklearn.model_selection import train_test_split


def LeNet_5(x):
    # TODO: Layer 1 : Convolutional Layer. Input = 32x32x1, Output = 28x28x1.
    conv1_w = tf.Variable(tf.truncated_normal(shape=[5, 5, 1, 6], mean=0, stddev=0.1))
    conv1_b = tf.Variable(tf.zeros(6))
    conv1 = tf.nn.conv2d(x, conv1_w, strides=[1, 1, 1, 1], padding= 'VALID') + conv1_b
    # TODO: Activation.
    conv1 = tf.nn.relu(conv1)
    # Pooling Layer. Input = 28x28x1. Output = 14x14x6.
    pool_1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding= 'VALID')

    # TODO: Layer 2: Convolutional. Output = 10x10x16.
    conv2_w = tf.Variable(tf.truncated_normal(shape=[5, 5, 6, 16], mean=0, stddev=0.1))
    conv2_b = tf.Variable(tf.zeros(16))
    conv2 = tf.nn.conv2d(pool_1, conv2_w, strides=[1, 1, 1, 1], padding= 'VALID') + conv2_b
    # TODO: Activation.
    conv2 = tf.nn.relu(conv2)
    # TODO: Pooling. Input = 10x10x16. Output = 5x5x16.
    pool_2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding= 'VALID')
    # TODO: Flatten. Input = 5x5x16. Output = 400.
    fc1 = flatten(pool_2)

    # TODO: Layer 3: Fully Connected. Input = 400. Output = 120.
    fc1_w = tf.Variable(tf.truncated_normal(shape=(400, 120), mean=0, stddev=0.1))
    fc1_b = tf.Variable(tf.zeros(120))
    fc1 = tf.matmul(fc1, fc1_w) + fc1_b
    # TODO: Activation.
    fc1 = tf.nn.relu(fc1)

    # TODO: Layer 4: Fully Connected. Input = 120. Output = 84.
    fc2_w = tf.Variable(tf.truncated_normal(shape=(120, 84), mean=0, stddev=0.1))
    fc2_b = tf.Variable(tf.zeros(84))
    fc2 = tf.matmul(fc1, fc2_w) + fc2_b
    # TODO: Activation.
    fc2 = tf.nn.relu(fc2)

    # TODO: Layer 5: Fully Connected. Input = 84. Output = 10.
    fc3_w = tf.Variable(tf.truncated_normal(shape=(84, 10), mean=0, stddev=0.1))
    fc3_b = tf.Variable(tf.zeros(10))
    logits = tf.matmul(fc2, fc3_w) + fc3_b
    return logits


def get_data(path):
    # 从csv中读取数据
    df_train = pd.read_csv(os.path.join(path, "train.csv"))
    # 提取图像数组和one-hot标签
    df_train = pd.get_dummies(df_train, columns=["label"])
    df_features = df_train.iloc[:, :-10].values
    df_label = df_train.iloc[:, -10:].values
    X_train, X_test, y_train, y_test = train_test_split(df_features, df_label, test_size=0.2, random_state=1212)
    # reformat train dataset
    train_dataset = X_train.reshape((-1, 28, 28, 1)).astype(np.float32)
    # reshape train dataset
    X_train = np.pad(train_dataset, ((0, 0), (2, 2), (2, 2), (0, 0)), 'constant')
    return X_train, y_train


if __name__ == "__main__":
    # 导入数据集
    X_train, y_train = get_data('../lenet_5/dataset')

    ### 开始构建图 ###
    x = tf.placeholder(tf.float32, shape=[None, 32, 32, 1])
    y_ = tf.placeholder(tf.int32, (None))
    logits = LeNet_5(x)
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_, logits=logits)
    loss_operation = tf.reduce_mean(cross_entropy)
    optimizer = tf.train.AdamOptimizer(learning_rate=0.001)
    training_operation = optimizer.minimize(loss_operation)
    correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(y_, 1))
    accuracy_operation = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    ### 结束构建图 ###

    # 初始化variables并开始训练
    EPOCHS = 10
    BATCH_SIZE = 128
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        num_examples = len(X_train)
        for i in range(EPOCHS):
            X_train, y_train = shuffle(X_train, y_train)
            for offset in range(0, num_examples, BATCH_SIZE):
                end = offset + BATCH_SIZE
                batch_x, batch_y = X_train[offset:end], y_train[offset:end]
                sess.run(training_operation, feed_dict={x: batch_x, y_: batch_y})
            print(sess.run(accuracy_operation, feed_dict={x: batch_x, y_: batch_y}))
        print(num_examples)
        saver = tf.train.Saver()
        save_path = saver.save(sess, 'model/lenet.ckpt')
        print(save_path)

