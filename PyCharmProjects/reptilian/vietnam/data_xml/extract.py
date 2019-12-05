import os
import re
import quopri
from xml.dom.minidom import Document
from bs4 import BeautifulSoup
from threading import Thread


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
    return img_list, content_list


# 写入xml文档
def write_xml(title, time, image, content, path=""):
    filename = path + '//' + title + '.xml'
    doc = Document()
    news = doc.appendChild(doc.createElement('news'))
    title_element = news.appendChild(doc.createElement('title'))
    title_element.appendChild(doc.createTextNode(title))
    time_element = news.appendChild(doc.createElement('time'))
    time_element.appendChild(doc.createTextNode(str(time)))
    content_element = news.appendChild(doc.createElement('content'))
    if len(image) != 0:
        for item in content:
            image_text = content_element.appendChild(doc.createElement('image'))
            image_text.appendChild(doc.createTextNode(str(item)))
    for item in content:
        p = content_element.appendChild(doc.createElement('p'))
        p.appendChild(doc.createTextNode(str(item)))
    with open(filename, 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
    f.close()


# 读取新闻文件夹
def get_list(filepath):
    result = os.listdir(filepath)
    return result


# 主函数
if __name__ == "__main__":
    read_path = "d://source"
    news_list = get_list(read_path)
    times_count = 0
    for item in news_list:
        file_name = read_path + "//" + item
        try:
            article = get_article(file_name)
            title, time, image, content = get_element(article)
            times_count = times_count + 1
            outstring = "已经进行" + str(times_count) + "次转换"
            print(outstring)
        except:
            times_count = times_count + 1
            outstring = "第" + str(times_count) + "次转换失败"
            print(outstring)
