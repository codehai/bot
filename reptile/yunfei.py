import requests
from bs4 import BeautifulSoup
import re

def format_score(score,race):

	zh_list = re.findall(r"\d+",score[u'赛鸽足环'])
	zuhuan = ['','-','','-','']
	for zh in zh_list:
		if len(zh) == 2:
			zuhuan[2] = zh
		elif len(zh) == 4:
			zuhuan[0] = zh
		else:
			zuhuan[4] = zh
	zuhuan = ''.join(zuhuan)
	print(score[u'名次'], race[u'比赛时间'], score[u'姓名'], score[u'归巢时间'], score[u'飞行速度'], score[u'实际空距'], race[u'所属协会'], zuhuan, score[u'鸽棚编号'], race[u'赛事名称'])

def get_race_score(table,race):

	score_name = ['名次', '姓名', '鸽棚编号', '赛鸽足环', '赛鸽资料', '归巢时间', '鸽棚经纬度', '实际空距', '飞行速度', '报到方式']
	tr_list = table.find_all('tr')
	for tr in tr_list[2:]:
		score_value = []
		for string in tr.stripped_strings:
			score_value.append(string)
		score = dict(zip(score_name,score_value))
		format_score(score,race)

def  get_race_item(url,race):

	url = 'http://www.yunfeichina.com/matchlive/%s' %(url)
	r = requests.get(url)
	r.encoding = 'utf-8'
	soup = BeautifulSoup(r.text,'lxml')
	table_list = soup.find_all('table')
	pages = re.findall(r"共(\d+)",table_list[3].div.text)
	current_page = re.findall(r"第(\d+)",table_list[3].div.text)
	if pages and current_page:
		get_race_score(table_list[2],race)
		next_page = int(current_page[0])+1
		if next_page > int(pages[0]):
			return
		else:
			next_url = '%s&page=%d' %(race['url'],next_page) 
			get_race_item(next_url,race)
	else:
		return

def  get_race(page,y_url,name):

	url = y_url + '&page=' + str(page)
	r = requests.get(url)
	r.encoding = 'utf-8'
	soup = BeautifulSoup(r.text,'lxml')
	table = soup.find('div',class_='city_two_right_x')
	tr_list = table.find_all('tr')
	pages = re.findall(r"/(\d+)",tr_list[-1].text.replace('\n',''))
	current_page = re.findall(r"(\d+)/",tr_list[-1].text.replace('\n',''))
	if pages and current_page:
		for index in range(2,len(tr_list) - 2):
			td_list = tr_list[index].find_all('td')
			race = {}
			race['赛事名称'] = td_list[0].text
			race['比赛时间'] = td_list[1].text
			'''
			添加时间检测
			'''
			race['放飞地'] = td_list[2].text
			race['天气'] = td_list[3].text
			race['赛段(km)'] = td_list[4].text
			race['url'] = td_list[5].a['href']
			race['所属协会'] = name
			get_race_item(race['url'],race)
		next_page = int(current_page[0]) + 1
		print(next_page)
		if next_page > int(pages[0]):
			return
		else:
			get_race(next_page,y_url,name)

def get_union():

	for id in range(1,37):
		'''不同的城市,获取各个协会,遍历各个协会下的比赛然后
		'''
		url = 'http://www.yunfeichina.com/matchlive/Yf_list.php?id=%d' %(id)
		r = requests.get(url)
		r.encoding = 'utf-8'
		soup = BeautifulSoup(r.text,'lxml')
		xh_div = soup.find('div',class_='city_two_left') #协会
		xh_list = xh_div.find_all('li')
		if xh_list:
			for xh in xh_list:#遍历协会
				url = 'http://www.yunfeichina.com/matchlive/%s' %(xh.a['href'])
				get_race(1,url,xh.text)

if __name__ == "__main__":
	get_union()

