#coding=utf-8

import requests
import json
import sys
import re
from bs4 import BeautifulSoup
from datetime import datetime, date, time

url = 'http://www.aj52zx.com/Racelist.aspx?page=1'
headers = {'User-Agent': 'NokiaN97/21.1.107 (SymbianOS/9.4; Series60/5.0 Mozilla/5.0; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebkit/525 (KHTML, like Gecko) BrowserNG/7.1.4'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
content = soup.find_all('table',id='ctl00_ContentPlaceHolder1_GridView1')
items = content[0].find_all('tr')

race_items = []
for item in items:
        race_item = []
        tds = item.find_all('td')
        a = tds[1].find_all('a')
        if len(a):
                href =  a[0]['href']
                race_item.append(href)
                for string in item.stripped_strings:
                        race_item.append(string)
                print json.dumps(race_item,ensure_ascii=False)
                race = {'organ':race_item[0],'item':race_item[1],'time':race_item[2],'site':race_item[3],'distance':race_item[4],'number':race_item[5],'coordinate':race_item[6],'homing':race_item[7],'weather':race_item[8],'url':url}
        race_items.append(race_item)
print len(race_items)

