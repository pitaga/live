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
    img_list, content_list = get_vietnam_text(text_list)
    return title, time, img_list, content_list


# 获取文字内容
def get_vietnam_text(text):
    img_list, content_list = [], []
    if text('div'):
        img_text = text.find_all('div')
        for item in img_text:
            img_list.append(item.get_text())
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
        for item in image:
            image_text = content_element.appendChild(doc.createElement('image'))
            image_text.appendChild(doc.createTextNode(str(item)))
    for item in content:
        p = content_element.appendChild(doc.createElement('p'))
        p.appendChild(doc.createTextNode(str(item)))
    with open(filename, 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
    f.close()


# 线程函数，用于提取mhtml中感兴趣内容
def mht_to_xml(file_name_list, read_path, save_path, thread_num):
    times_count = wrong_times = 0
    for item in file_name_list:
        file_name = read_path + "//" + item
        try:
            article = get_article(file_name)
            title, time, image, content = get_element(article)
            write_xml(title, time, image, content, save_path)
            times_count = times_count + 1
        except:
            times_count = times_count + 1
            wrong_times = wrong_times + 1
        if times_count%1000 == 0:
            outstring = "线程" + str(thread_num) + "已进行" + str(times_count) + "次，失败" + str(wrong_times) + "次。"
            print(outstring)


# 读取新闻文件夹
def get_list(filepath):
    result = os.listdir(filepath)
    return result


# 主函数
if __name__ == "__main__":
    read_path = "e://source"
    save_path = "e://save"
    news_list = get_list(read_path)
    t1 = Thread(target=mht_to_xml, args=(news_list[:10000], read_path, save_path, 1))
    t2 = Thread(target=mht_to_xml, args=(news_list[10000:20000], read_path, save_path, 2))
    t3 = Thread(target=mht_to_xml, args=(news_list[20000:30000], read_path, save_path, 3))
    t4 = Thread(target=mht_to_xml, args=(news_list[30000:40000], read_path, save_path, 4))
    t5 = Thread(target=mht_to_xml, args=(news_list[40000:], read_path, save_path, 5))
    t1.start(), t2.start(), t3.start(), t4.start(), t5.start()
    t1.join(), t2.join(), t3.join(), t4.join(), t5.join()
