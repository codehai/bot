import requests
import json
import sys
import re
from bs4 import BeautifulSoup
from datetime import datetime, date, time
import urllib2
from types import NoneType
from urllib import urlencode


url='https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%E6%BB%9A%E8%BD%AE&rsv_pq=ab69858100042aa5&rsv_t=be53oRF%2B0dU22YzHgQkvl4cKLZxwB1UBLL2VZiUZdaubji9oUrW9BtNOJ8w&rqlang=cn&rsv_enter=1&rsv_sug3=12&rsv_sug1=17&rsv_sug7=100&rsv_sug2=0&inputT=6897&rsv_sug4=6970'
headers = {'User-Agent': 'Mozilla/5.0_(iPod;_U;_CPU_iPhone_OS_4_3_1_like_Mac_OS_X;_zh-cn)_AppleWebKit/533.17.9_(KHTML,_like_Gecko)_Version/5.0.2_Mobile/8G4_Safari/6533.18.5'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
content = soup.find_all('div',id='rs')
items =  content[0].find_all('a')
for item in items:
    print item['href']
    for string in item.stripped_strings:
        print string