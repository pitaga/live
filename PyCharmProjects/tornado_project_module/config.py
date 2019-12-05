'''
    配置文件，用于配置options选项和settings等
'''

import os
BASE_DIR = os.path.dirname(__file__)    # 生成当前目录所在的绝对路径


# 参数
options = {
    "port": 7000
}

# 配置
settings = {
    "static_path": os.path.join(BASE_DIR, "static"),
    "template_path": os.path.join(BASE_DIR, "templates"),
    # 设置tornado是否工作在调试模式下，默认为false即工作在生产模式下
    "debug": True
}