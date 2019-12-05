import re


source_path = "../vietnam/result.txt"
result_path = "../vietnam/print.txt"
header = "https://www.vietnamplus.vn/Utilities/Print.aspx?contentid="
pat = r'(?<=\/)[0-9]+?(?=\.vnp)'

file = open(source_path, 'r')
lst = file.read().split()
file.close()

result = open(result_path, "a+")
for item in lst:
    result.write(header + re.findall(pat, item)[0] + '\n')
result.close()
