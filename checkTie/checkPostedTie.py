#coding=utf-8

import postgres
import editDistance
import requests
import json
import sys
import re
from bs4 import BeautifulSoup
from datetime import datetime, date, time

# minute
DELTA_TIME = 100
DELTA_EDIT = 10

def checkPostedTie(tie):
	headers = {'User-Agent': 'NokiaN97/21.1.107 (SymbianOS/9.4; Series60/5.0 Mozilla/5.0; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebkit/525 (KHTML, like Gecko) BrowserNG/7.1.4'}
	# print tie[0]
	obj = tie[4]
	# print obj
	# obj = json.loads(tie["tie"])
	r = requests.get(obj["url"], headers=headers)
	# print r.text

	soup = BeautifulSoup(r.text, 'html.parser')
	# file = open("out", "w")
	# file.write(soup.prettify().encode('utf-8'))
	# file.close();
	# # print soup.prettify()

	ties = soup.find_all("div", class_="i")
	postContent = obj["content"]
	postUser = tie[2].encode("utf-8")
	# print postUser
	postTime = re.findall('\d+-\d+-\d+T\d+:\d+',tie[1])
	# print postTime
	postTime = datetime.strptime(postTime[0],"%Y-%m-%dT%H:%M")
	if len(ties)==0:
		postgres.addRevisitedTie(tie[0], json.dumps("{}"), 2, 0)
		return
	for t in ties:
		texts = []
		log = {}
		for string in t.stripped_strings:
			texts.append(string)
		# print json.dumps(texts,ensure_ascii=False)
		textsLen = len(texts)
		if texts[textsLen - 1] == u"回复":
			texts.pop()
			textsLen = textsLen - 1
		tieUser = texts[textsLen - 2]
		if postUser != tieUser.encode("utf-8"):
			continue
		if t.find_all("img",class_="BDE_Image"):
			img = 1
		else:
			img = 0
		tieTime = texts[textsLen - 1]
		# dt = datetime.strptime(tieTime, "%m-%d %H:%M")
		# dt = dt.replace(year = datetime.now().year)
		# deltaTime = abs((dt - postTime).total_seconds())
		# if deltaTime > DELTA_TIME*60:
		# 	pass
		# 	# continue
		# log["time"] = deltaTime / 1000
		dotIndex = texts[0].find(".")
		tieContent = texts[0][dotIndex+1:] + "".join(texts[1:textsLen-2])
		contentDistance = editDistance.getEditDistance(postContent, tieContent)
		if contentDistance > DELTA_EDIT:
			continue
		log["distance"] = contentDistance
		postgres.addRevisitedTie(tie[0], json.dumps(log), 0,img)
		return
	postgres.addRevisitedTie(tie[0], json.dumps("{}"), 1, 0)

# postedTies = postgres.findTies()
# for tie in postedTies:
# 	checkPostedTie(tie)
# 	break

while True:
	tie = json.loads(sys.stdin.readline())

	if not tie:
		break
	try:		
		checkPostedTie(tie)
	except Exception, e:
		raise


# obj = {"content":"『最美的笑颜』『自然的演技』『直爽的性格』『灵魂主唱——郑恩地』【恩地吧宝石：小慧】", "url":"http://tieba.baidu.com/p/4531052199?lp=5028&mo_device=1&is_jingpost=0&pn=0&"}

# print json.dumps(obj)











