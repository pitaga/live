import os
import glob
import tensorflow as tf
from tensorflow.python.platform import gfile


# 重命名图片名称，以方便保存
def replace_name(name, replace):
    name_list = name.split("\\")
    name_list[-1] = replace + name_list[-1]
    file_name = "\\".join(name_list)
    return file_name


# 图像数量扩张
def ImageProcess(INPUT_DATA):
    for sub_dir in [x[0] for x in os.walk(INPUT_DATA)][1:]:
        # 获取一个子目录中所有的图片文件。
        file_list = []
        dir_name = os.path.basename(sub_dir)
        for extension in ['jpg', 'jpeg']:
            file_glob = os.path.join(INPUT_DATA, dir_name, '*.' + extension)
            file_list.extend(glob.glob(file_glob))      # 路径和文件名加入file_list列表

        # 遍历图片目录所有图片
        for file_name in file_list:
            with tf.Session() as sess:
                # 裁剪图片为299*299
                image_raw_data = gfile.FastGFile(file_name, 'rb').read()
                image_data = tf.image.decode_jpeg(image_raw_data)
                image_resize = tf.image.resize_image_with_crop_or_pad(image_data, 299, 299)

                # 写入保存裁剪后图片
                encoded_image = tf.image.encode_jpeg(image_resize)
                with tf.gfile.GFile(file_name, 'wb') as f:
                    f.write(encoded_image.eval())
                print(file_name + " has been prccessed.")

                # 随机左右翻转，并保存旋转后图片
                image_process = tf.image.random_flip_left_right(image_resize)
                encoded_image = tf.image.encode_jpeg(image_process)
                file_name = replace_name(file_name, "left_right_")
                with tf.gfile.GFile(file_name, 'wb') as f:
                     f.write(encoded_image.eval())
                print(file_name + " has been prccessed.")

                # 随机上下翻转，并保留旋转后的图片
                image_process = tf.image.random_flip_up_down(image_resize)
                encoded_image = tf.image.encode_jpeg(image_process)
                file_name = replace_name(file_name, "up_down_")
                with tf.gfile.GFile(file_name, 'wb') as f:
                    f.write(encoded_image.eval())
                print(file_name + " has been prccessed.")

                # 随机光暗调整，并保存调整后的图片
                image_process = tf.image.random_brightness(image_resize, 0.4)
                encoded_image = tf.image.encode_jpeg(image_process)
                file_name = replace_name(file_name, "brightness_")
                with tf.gfile.GFile(file_name, 'wb') as f:
                    f.write(encoded_image.eval())
                print(file_name + " has been prccessed.")

                # 随机数据增强，并保存调整后的图片
                image_process = tf.image.random_hue(image_resize, 0.4)
                encoded_image = tf.image.encode_jpeg(image_process)
                file_name = replace_name(file_name, "hue_")
                with tf.gfile.GFile(file_name, 'wb') as f:
                    f.write(encoded_image.eval())
                print(file_name + " has been prccessed.")


if __name__ == "__main__":
    ImageProcess("data")