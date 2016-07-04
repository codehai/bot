#coding=utf-8

from datetime import date
import time
from random import choice
import postgres
import json
import sys
import types


LOG_EXTRACT_KEY = "cookieJar"
LOG_EXTRACT_KEY_CHILD = "cookies"
LOG_UA = "ua"
LOG_UN = "un"

# if len(sys.argv) < 2:
# 	print "..............please input log name.............."
	

logFile = open(sys.argv[1])
jsonStr = logFile.read()

# testFile = open("testFile", 'w')
# testFile.write(jsonStr)
# testFile.close()

jsonObject = json.loads(jsonStr)
logFile.close()


# print sys.argv[2]

ua_un = ""
# print "jsonObject" + str(len(jsonObject)) 
cookiesJarNum = 0
for i in range(len(jsonObject)) :
	cur = jsonObject[i]
	if isinstance(cur, dict) and len(cur) == 2 and cur.has_key(LOG_UA) and cur.has_key(LOG_UN):
		ua_un = (cur)

	if isinstance(cur, unicode) :
		isFirst = False
		for j in range(i+1, len(jsonObject)) :
			if isFirst :
				break
			if isinstance(jsonObject[j], dict) :
				# to find possible dict
				isFirst = True
				for key, value in jsonObject[j].items() :
					if key == LOG_EXTRACT_KEY and isinstance(value, dict) :
						# print "........" + str(i)
						cookiesJarNum += 1
						# for k, v in value.items() :
							# if k == LOG_EXTRACT_KEY_CHILD :
								# if len(sys.argv) == 2 :
									# postgres.addLogCookiesDefault(ua_un, json.dumps(v))
									# print json.dumps(v)
								# else :
									# postgres.addLogCookies(ua_un, json.dumps(v), json.loads(sys.argv[2]))
									# print json.dumps(v)
									# print json.loads(sys.argv[2])

count = 0
if cookiesJarNum== 0:
	if ua_un:
		v=[""]
		postgres.addLogCookies(ua_un, json.dumps(v[0]), json.loads("{}"))
	else:
		v=[""]
		ua_un = {"un":"","ua":""}
		postgres.addLogCookies(ua_un, json.dumps(v[0]), json.loads("{}"))
else:
	for i in range(len(jsonObject)) :
		cur = jsonObject[i]
		if isinstance(cur, dict) and len(cur) == 2 and cur.has_key(LOG_UA) and cur.has_key(LOG_UN):
			ua_un = (cur)

		if isinstance(cur, unicode) :
			isFirst = False
			for j in range(i+1, len(jsonObject)) :
				if isFirst :
					break
				if isinstance(jsonObject[j], dict) :
					# to find possible dict
					isFirst = True
					for key, value in jsonObject[j].items() :
						if key == LOG_EXTRACT_KEY and isinstance(value, dict) :
							# print "........" + str(i)
							count += 1
							if count == cookiesJarNum:
								for k, v in value.items() :
									if k == LOG_EXTRACT_KEY_CHILD :
										if len(sys.argv) == 2 :
											postgres.addLogCookies(ua_un, json.dumps(v), json.loads("{}"))
											
										else :
											postgres.addLogCookies(ua_un, json.dumps(v), json.loads(sys.argv[2]))
											














