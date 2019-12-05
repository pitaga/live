import re


filename = "../vietnam/source.mhtml"
pat = r'(?<=<article class=3D"article">)[\S\s]*?(?=</article>)'


file = open(filename, 'r')

html = file.read()
lst = re.findall(pat, html)
for i in lst:
    print(i)
file.close()