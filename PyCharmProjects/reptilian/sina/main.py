from reptilian.sina.newstools import *
import re

if __name__ == "__main__":
    res = requests.get('http://news.sina.com.cn/')              # 新浪新闻网址
    res.encoding = ('utf-8')                                    # 编码方法
    soup = BeautifulSoup(res.text, 'html.parser')

    lst = soup.find_all('a', target="_blank", href=re.compile(".*doc.*"))
    for link in lst:
        print(link.get('href'))
