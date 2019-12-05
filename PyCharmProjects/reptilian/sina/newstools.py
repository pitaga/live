import requests
from bs4 import BeautifulSoup


def get_news(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        lst = soup.find_all('p', class_="")
        print("==================================================================================")
        for i in lst:
            print(i.text)
        print("==================================================================================")
    except:
        print("获取新闻失败")