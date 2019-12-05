import os                               #解决AVX报错
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf                 #导入tensorflow库

sess = tf.InteractiveSession()          #创建交互式会话
input1 = tf.placeholder(tf.float32)     #创建占位符
input2 = tf.placeholder(tf.float32)     #创建占位符
res = tf.multiply(input1, input2)       #创建乘法操作
res.eval(feed_dict={input1:[7.], input2:[2.]})  #求值