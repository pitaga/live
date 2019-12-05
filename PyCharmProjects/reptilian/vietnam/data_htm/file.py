'''
    此文件用于读写文件测试
'''


'''txt文件追行读取文件内容到列表'''
# path = "../vietnam/urls.txt"
#
# file = open(path, 'r')
# result = file.read().split()
# for item in result:
#     print(item)


'''txt文件追加写入'''
path = "../vietnam/log.txt"
file = open(path, 'a+')
file.write("test")