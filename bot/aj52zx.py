#coding=utf-8

import requests
import json
import sys
import re
from bs4 import BeautifulSoup
from datetime import datetime, date, time
import urllib2
from types import NoneType

def score(score_soup,score_name,pagenum,race):
        try:
                score_content = score_soup.find_all('td')
                td_strings = []
                for td in score_content:
                        td_strings.append(td.string)
                t = 0
                score = []
                scores = []
                for num in range(td_strings.index(str(pagenum*300+1)),len(td_strings)):
                        # print td_strings[num]
                        if not isinstance(td_strings[num],NoneType):
                                score.append(td_strings[num].strip(' '))
                        else:
                                score.append(td_strings[num])
                        t+=1
                        if t>11:
                                # print json.dumps(score,ensure_ascii=False,indent=2)
                                score_obj = dict(zip(score_name,score))
                                del score_obj[u'暗码']
                                del score_obj[u'当前坐标']
                                del score_obj[u'插组']
                                del score_obj[u'空距']
                                del score_obj[u'团体']
                                del score_obj[u'鸽舍坐标']
                                score_obj[u'比赛名称'] = race[u'比赛项目']
                                score_obj[u'所属单位'] = race[u'举办赛事组织']
                                score_obj[u'司放时间'] = race[u'司放时间']
                                score_obj[u'空距/KM'] = race[u'空距/KM']
                                scores.append(score_obj)
                                score = []
                                t = 0
                return scores
        except ValueError:
                return scores
                pass
        except Exception, e:
                raise
        
url = 'http://www.aj52zx.com/Racelist.aspx?page=1'
headers = {'User-Agent': 'Mozilla/5.0_(iPod;_U;_CPU_iPhone_OS_4_3_1_like_Mac_OS_X;_zh-cn)_AppleWebKit/533.17.9_(KHTML,_like_Gecko)_Version/5.0.2_Mobile/8G4_Safari/6533.18.5'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
content = soup.find_all('table',id='ctl00_ContentPlaceHolder1_GridView1')
items = content[0].find_all('tr')
item_name = ['url',u'举办赛事组织',u'比赛项目',u'司放时间',u'司放地点',u'空距/KM',u'上笼羽数',u'司放地坐标',u'当前归巢',u'司放天气']
score_name = [u'名次',u'鸽主姓名',u'棚号',u'足环号码',u'暗码',u'归巢时间',u'空距',u'分速',u'鸽舍坐标',u'当前坐标',u'团体',u'插组']
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
                race = dict(zip(item_name,race_item))
                # print json.dumps(race,ensure_ascii=False,indent=2)
                race_items.append(race)
# print json.dumps(race_items,ensure_ascii=False,indent=2) #比赛项目
for race in race_items:
                scores = []
                score_url = 'http://www.aj52zx.com/'+race['url']
                score_html = urllib2.urlopen(score_url).read()
                score_soup = BeautifulSoup(score_html,'html.parser')
                # print(score_soup.prettify())
                page = score_soup.find_all('a',class_='manu')
                scores = score(score_soup,score_name,0,race)
                for pagenum in page:
                        if re.findall('\d',pagenum.string):
                                print pagenum.string
                                score_url = 'http://www.aj52zx.com/'+race['url']+'&page='+pagenum.string
                                score_html = urllib2.urlopen(score_url).read()
                                score_soup = BeautifulSoup(score_html,'html.parser')
                                # print score_soup
                                score_child = score(score_soup,score_name,int(pagenum.string)-1,race)
                                print json.dumps(score_child,ensure_ascii=False,indent=2) #比赛成绩
                                scores.extend(score_child)
                if not isinstance(scores,NoneType):
                        print len(scores)    
                        if len(scores):
                                print json.dumps(scores,ensure_ascii=False,indent=2) #比赛成绩    
                                break


