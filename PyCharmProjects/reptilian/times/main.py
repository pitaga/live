import requests


kv = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
url = "https://www.nytimes.com/"

r = requests.get(url=url, timeout=100, headers=kv)
r.raise_for_status()
r.encoding = r.apparent_encoding
print(r.text)

