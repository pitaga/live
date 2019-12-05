import re


pat1 = r'(?<=dir).*(?=dur)'
pat = r'[a-z]+'

mess = b'{"dir":"down", "dur":undefined}'

data = mess.decode('utf-8')

str = re.findall(pat1, data)[0]
direction = re.findall(pat, str)[0]

print(direction)