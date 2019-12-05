'''
      此文件用于正则表达式测试
'''

import re

str = '<a href="/xe-buyt-roi-xuong-vuc-sau-hang-tram-met-it-nhat-8-nguoi-tu-vong/544116.vnp">' \
      '<h2 class="title">Xe buýt rơi xuống vực sâu hàng trăm mét, ít nhất 8 người tử vong</h2>' \
      '</a>'

pat = r'(?<=<a href=\")\/[a-z0-9\-]+\/[0-9]+\.vnp?(?=\")'
print(re.findall(pat, str))