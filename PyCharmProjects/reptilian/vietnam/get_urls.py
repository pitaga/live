'''
    此文件用于爬取链接（广度搜索）
'''


import requests
import re


kv = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'}
pattern = r'(?<=<a href=\")\/[a-z0-9\-]+\/[0-9]+\.vnp?(?=\")'
title = "https://www.vietnamplus.vn/"


# 广搜网页获取当前网页所有新闻链接
def get_vietnam_urls(url):
    result = []
    try:
        r = requests.get(url, headers=kv, timeout=100)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        lst = re.findall(pattern, r.text)
        for index in range(len(lst)):
            result.append(title + lst[index])
    except:
        print("爬去失败")
    return result


# 读取start_urls
def read_urls(path):
    file = open(path, 'r')
    result = file.read().split()
    file.close()
    return result


# 写入result
def write_urls(path, news_list):
    file = open(path, 'w')
    for item in news_list:
        file.write(item + "\n")
    file.close()


# 主函数
if __name__ == "__main__":
    source_path = "../vietnam/start.txt"
    result_path = "../vietnam/result.txt"
    start_list = read_urls(source_path)
    result_list = read_urls(result_path)
    urls = list(set(result_list) - set(start_list))
    count_times, lenth, result = 0, len(urls), result_list
    for item in urls:
        count_times = count_times + 1
        result += get_vietnam_urls(item)
        outstring = "当前循环" + str(count_times) + "/" + str(lenth) + "次, 已经爬取" + str(len(result)) + "条url。"
        print(outstring)
        if count_times%500 == 0:
            print("====================================================")
            result = list(set(result))
            write_urls(result_path, result)
            print("result.txt写入完成。")
            write_urls(source_path, start_list+urls[:count_times])
            print("start.txt数据已经更新。")
            print("====================================================")