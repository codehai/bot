#coding=utf-8

import requests
from datetime import date
import time
from random import choice
import postgres


keys = []
keyCount = []

keyFile = open("keys")
for line in keyFile.readlines() :
	obj = line.split(":")
	if len(obj) == 2 :
		keys.append(obj[0])
		keyCount.append(int(obj[1]))
keyFile.close()


day = date.today().day
params = {}
postCount = 0


def initKeys() :
	keyFile = open("keys", "w")
	keyFile.write("562d3f18d062605746fb121d71d120aa : 0\n")
	keyFile.write("053924905517d71e41cc597315329e7d : 0\n")
	keyFile.write("4377c2667acb0e3dea56a030e551a699 : 0\n")
	keyFile.write("e2bc6e39ce82bc6354aaf33e1d1ef5c8 : 0\n")
	keyFile.write("3ad6f930a5fa20a44cca94bb7a3a2033 : 0\n")
	keyFile.close()
# initKeys()



def saveKeys() :
	global keys
	global keyCount
	keyFile = open("keys", "w")
	for i in range(len(keys)) :
		keyFile.write(keys[i] + ":" + str(keyCount[i]) + "\r\n")
	keyFile.close()



def chat(message) :

	# print message
	# return 
	global postCount
	global keyCount
	global keys

	userInput = message
	# dbResult = postgres.findByQ(userInput)
	# if len(dbResult) > 0 :
	# 	# temp = choice(dbResult)
	# 	# print temp['a']
	# 	print "......"
	# 	return

	if len(userInput) < 100 :
		params["info"] = userInput
	else :
		return

	# print userInput
	# curDay = date.today().day
	# if curDay != day :
	# 	for cnt in keyCount :
	# 		cnt = 0
	usefulKey = []
	for i in range(len(keyCount)) :
		if keyCount[i] < 5000 :
			usefulKey.append(keys[i])
	if len(usefulKey) < 1 :
		print "all keys are invalid..."
		time.sleep(2)
		return


	j = choice(range(len(usefulKey)))
	keyCount[j] = keyCount[j] + 1
	params["key"] = keys[j]
	r = requests.post("http://www.tuling123.com/openapi/api", params=params)
	saveKeys()
	aJson = None
	try :
		aJson = r.json()
	except ValueError, e :
		print e
		time.sleep(2)
		return


	# print aJson
	postCount = postCount + 1
	# print "post: " + str(postCount)


	a = ""
	if "code" in aJson and aJson["code"] == 100000  :
		a = aJson["text"]
	elif "100000" in aJson :
		a = aJson["100000"]
	else :
		return
	dbResult = postgres.findByQandA(userInput, a)
	if len(dbResult) == 0 :
		postgres.add(userInput, a)
	return a
	# print
	# print


# while True:
# 	userInput = raw_input("--->")
# 	chat(userInput)


def dumpA() :
	aList = postgres.getFreqA(1)
	f = open("a." + str(postgres.getQACount()), 'w')
	for a in aList :
		f.write(a['a'] + "\t" + str(a['cnt']) + "\n")
	f.close()
# dumpA()



def chatFromDB() :
	limit = 1000
	cnt = 0
	for i in range(postgres.getTiebaCount() / limit + 1) :
		tiebas = postgres.findTieba(i * limit, limit)
		for tieba in tiebas :
			post = tieba["post"]
			cnt = cnt + 1
			print "tiebas: " + str(cnt)
			if len(post) > 0 :
				chat(post)
			print 
			# time.sleep(0.2)
	dumpA()
# chatFromDB()




# qas = postgres.findByA("对不起，没听清楚，请再说一遍吧。")
# for qa in qas :
# 	print qa["q"]
# 	raw_input()

# qas = postgres.findByQ("盖好被子，晚安")
# for qa in qas :
# 	print qa["a"]
# 	raw_input()








# print postgres.findTieba()

# postgres.add("hello", "你好")
# rtn = postgres.findByQ("hello")
# rtn = postgres.selectAll()
# for item in rtn :
# 	print item['q']
# 	print item['a']
# 	print item['t']
# print len(rtn)
# print rtn












