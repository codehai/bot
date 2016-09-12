import requests
import json
from bs4 import BeautifulSoup

color = []
for page in range(22,23):
	url = 'http://www.peise.net/color/'+str(page)+'.html'
	print(url)
	r = requests.get(url)
	r.encoding = 'gbk'
	soup = BeautifulSoup(r.text,'lxml')
	# print(soup)
	lis = soup.find_all('li',class_='indexcolor')
	obj = {}
	for li in lis:
		obj['color-name'] = li.h3.text
		print(obj['color-name'])
		obj['HEX'] = li.h4.text.replace('HEX:','')
		with open('color.txt','a') as file:
			file.write(str(obj)+'\n')
