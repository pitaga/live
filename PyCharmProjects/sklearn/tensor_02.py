import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf             #导入tensorflow库

a = tf.Variable([1.0, 2.0])         #创建常量数组
b = tf.Variable([3.0, 4.0])         #创建常量数组

sess = tf.InteractiveSession()      #创建交互式对话
sess.run(tf.global_variables_initializer()) #变量初始化
res = tf.add(a, b)                  #创建加法操作
print(res.eval())                   #执行操作并输出结果
sess.close()                        #关闭session