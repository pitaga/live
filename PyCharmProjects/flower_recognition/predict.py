import tensorflow as tf
import numpy as np


def predict():
    strings = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']
    def id_to_string(node_id):
        return strings[node_id]
    # 载入图
    with tf.gfile.FastGFile('model/model.pb', 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('output/prob:0')
        # 载入图片
        image_data = tf.gfile.FastGFile("image/test.png", 'rb').read()
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})  # 图片格式是jpg格式
        predictions = np.squeeze(predictions)  # 把结果转为1维数据
        """
        for node_id in top_k:
            # 获取分类名称
            human_string = id_to_string(node_id)
            # 获取该分类的置信度
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))
        print()
        """
        # 从大到小排序
        top_k = predictions.argsort()[::-1]
        return id_to_string(top_k[0])