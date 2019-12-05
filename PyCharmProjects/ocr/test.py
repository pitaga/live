# 调用tensorflow模型进行预测
import tensorflow as tf
import numpy as np
from tensorflow.contrib.layers import flatten


class Predict():
    # LeNet-5卷积神经网络
    def LeNet_5(self, x):
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

    # 载入模型并开始预测
    def predict(self, image):
        tf.reset_default_graph()
        x = tf.placeholder(tf.float32, shape=[None, 32, 32, 1])
        logits = self.LeNet_5(x)
        saver = tf.train.Saver()
        with tf.Session() as sess:
            saver.restore(sess, "model/lenet.ckpt")
            # 格式化输入图像
            submission_test = np.reshape(image, (1, 32, 32, 1)).astype(np.float32)
            Z = logits.eval(feed_dict={x: submission_test})
            y_pred = np.argmax(Z, axis=1)
        return y_pred[0]
