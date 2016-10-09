import requests
from bs4 import BeautifulSoup
import re

def  get_race_item(race):
	url = 'http://www.yunfeichina.com/matchlive/%s' %(race['url'])
	r = requests.get(url)
	r.encoding = 'utf-8'
	soup = BeautifulSoup(r.text,'lxml')
	table_list = soup.find_all('table')
	print(len(table_list))
	print(table_list[3].div.text)
	pages = re.findall(r"共(\d+)",table_list[3].div.text)
	if pages:
		print(int(pages[0]))
	else:
		return


def  get_race(tr_list):
	for index in range(2,len(tr_list)):
		td_list = tr_list[index].find_all('td')
		race = {}
		race['赛事名称'] = td_list[0].text
		race['比赛时间'] = td_list[1].text
		race['放飞地'] = td_list[2].text
		race['天气'] = td_list[3].text
		race['赛段(km)'] = td_list[4].text
		race['url'] = td_list[5].a['href']
		get_race_item(race)
		if index>2:
			break

for id in range(1,37):
	url = 'http://www.yunfeichina.com/matchlive/Yf_list.php?id=%d' %(id)
	r = requests.get(url)
	r.encoding = 'utf-8'
	soup = BeautifulSoup(r.text,'lxml')
	xh_div = soup.find('div',class_='city_two_left')
	xh_list = xh_div.find_all('li')
	if xh_list:
		for xh in xh_list:
			url = 'http://www.yunfeichina.com/matchlive/%s' %(xh.a['href'])
			r = requests.get(url)
			r.encoding = 'utf-8'
			soup = BeautifulSoup(r.text,'lxml')
			table = soup.find('div',class_='city_two_right_x')
			tr_list = table.find_all('tr')
			pages = int(re.findall(r"/(\d+)",tr_list[-1].text.replace('\n',''))[0])
			get_race(tr_list)
			if pages==1:
				break
			else:
				for page in range(2,pages+1):
					print(page)
			break
		break

