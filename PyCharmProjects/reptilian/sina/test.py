from urllib import request


head = {"User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0"}
proxy = {'http':'106.46.136.112:808'}
# url = "https://s.taobao.com/search?q=%E7%BE%BD%E7%BB%92%E6%9C%8D&style=grid"


url = 'http://www.whatismyip.com.tw/'

proxy_support = request.ProxyHandler(proxy)
opener = request.build_opener(proxy_support)
opener.addheaders = [('User-Agent', head['User-Agent'])]
request.install_opener(opener)
response = request.urlopen(url)

html = response.read().decode('utf-8')
print(html)