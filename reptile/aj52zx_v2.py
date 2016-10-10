import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, date, time
import sys

HEADERS = {'User-Agent': 'Mozilla/5.0_(iPod;_U;_CPU_iPhone_OS_4_3_1_like_Mac_OS_X;_zh-cn)_AppleWebKit/533.17.9_(KHTML,_like_Gecko)_Version/5.0.2_Mobile/8G4_Safari/6533.18.5'}
ITEM_NAME = ['举办赛事组织','比赛项目','司放时间','司放地点','空距','上笼羽数']
SCORE_NAME = ['名次', '鸽主姓名', '棚号', '足环号码', '暗码', '归巢时间', '空距', '分速(米/分)']

def get_score(page, url, race):
	url = 'http://www.aj52zx.com/%s&page=%d' %(url,page)
	r = requests.get(url, headers=HEADERS)
	soup = BeautifulSoup(r.text, 'lxml')
	table = soup.find('table')
	current_page = re.findall(r"(\d+)/",soup.find('div',class_='page').text)
	pages = re.findall(r"/(\d+)",soup.find('div',class_='page').text)
	tr_list = table.find_all('tr')
	if len(tr_list) < 2:
		return
	for tr in tr_list[1:]:
		score_value = []
		for string in tr.stripped_strings:
			score_value.append(string)
		score = dict(zip(SCORE_NAME,score_value))
		print(score)
	if current_page and pages:
		next_page = int(current_page[0]) + 1
		if next_page > int(pages[0]):
			return
		else:
			get_score(next_page, race['url'], race)


def get_race_item(url, date_set):

	for page in range(1,345):
		target_url = '%s?page=%d' %(url, page)
		print(target_url)
		r = requests.get(target_url, headers=HEADERS)
		soup = BeautifulSoup(r.text, 'lxml')
		table = soup.find('table')
		tr_list = table.find_all('tr')
		for tr in tr_list[1:]:
			item_value = []
			for string in tr.stripped_strings:
				item_value.append(string)
			race = dict(zip(ITEM_NAME,item_value))
			race['司放时间'] = datetime.strptime(race['司放时间'] ,'%Y/%m/%d %H:%M:%S').isoformat()
			td_list = tr.find_all('td')
			race['url'] = td_list[1].a['href']
			print(race['司放时间'])

			date_find = datetime.strptime(race['司放时间'].split('T')[0], "%Y-%m-%d")
			date_limit = datetime.strptime(date_set, "%Y-%m-%d")
			date_distance = (date_find - date_limit).total_seconds()

			if date_distance < 0:
				sys.exit(1)
			print(date_distance)
			'''
				添加时间检测
			'''
			get_score(1, race['url'], race)
			
		


if __name__ == "__main__":
	url = 'http://www.aj52zx.com/racelist.aspx'
	date_set = sys.argv[1]
	get_race_item(url,date_set)

