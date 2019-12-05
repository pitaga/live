import quopri
import re
from bs4 import BeautifulSoup

# 提取mhtml文档中的article部分
def get_article(filename):
    pat = r'(?<=<article class=3D"article">)[\S\s]*?(?=</article>)'
    file = open(filename, 'r')
    html = file.read()
    lst = re.findall(pat, html)
    return lst[0]


# 获取xml文档
def get_element(source):
    html = quopri.decodestring(source).decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find('h1').text[1:-1]
    time = soup.find('time').text
    text_list = soup.find('div', "article-body")
    img_list, content_list = get_text(text_list)
    return title, time, img_list, content_list


# 获取文字内容
def get_text(text):
    img_list, content_list = [], []
    if text('div'):
        img_text = text.find_all('div')
        for item in img_text:
            img_list += item.get_text()
        [s.extract() for s in text('div')]
    [s.extract() for s in text('br')]
    [s.extract() for s in text(None)]
    content = text.get_text()
    content_list = content.split('\n')
    content_list = [x for x in content_list if x!='']
    for i in content_list:
        print(i, type(i))
    return img_list, content_list


if __name__ == "__main__":
    out = get_article("../vietnam/test.mhtml")
    a, b, c, d = get_element(out)