import requests
from bs4 import BeautifulSoup
from xml.dom.minidom import Document


url = "https://www.vietnamplus.vn//nganh-su-pham-rot-tham-bo-giao-duc-va-dao-tao-hop-khan/461187.vnp"

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
header = soup.find("header", "article-header")
body = soup.find("div", "article-body cms-body AdAsia")


doc = Document()

news = doc.appendChild(doc.createElement('news'))


title = news.appendChild(doc.createElement('title'))
title.appendChild(doc.createTextNode(header.find('h1').text))
place = news.appendChild(doc.createElement('place'))
place.appendChild(doc.createTextNode(header.find('p').find('span').text))
time = news.appendChild(doc.createElement('time'))
time.appendChild(doc.createTextNode(header.find('p').find('time').text))
author = news.appendChild(doc.createElement('author'))
author.appendChild(doc.createTextNode(header.find('p').find('a').text))

content = news.appendChild(doc.createElement('content'))
for item in body.children:
    if item.string and item!='\n':
        p = content.appendChild(doc.createElement('p'))
        p.appendChild(doc.createTextNode(item.string))

filename = "text.xml"
with open(filename, 'wb') as f:
    f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))