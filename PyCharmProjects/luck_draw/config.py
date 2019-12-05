import os
BASE_DIR = os.path.dirname(__file__)


# 参数
options = {
    "port": 8000
}

settings = {
    "debug": True,
    "template_path": os.path.join(BASE_DIR, "templates"),
}