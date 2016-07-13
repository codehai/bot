#coding=utf-8

from datetime import date
import time
from random import choice
import postgres
import json
import sys
import types


LOG_SUCCESS = "success at last"
LOG_ERROR = "timeout"
LOG_ERROR_1 = "Timeout"
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
for i in range(len(jsonObject)) :
	cur = jsonObject[i]
	if isinstance(cur, dict) and len(cur) == 2 and cur.has_key(LOG_UA) and cur.has_key(LOG_UN):
		ua_un = (cur)

	state = -1
	if isinstance(cur, unicode) :
		if cur == LOG_SUCCESS :
			state = 0
		elif (cur.find(LOG_ERROR) != -1 or cur.find(LOG_ERROR_1) != -1) and (cur.find(LOG_ERROR) == (len(cur) - len(LOG_ERROR)) or cur.find(LOG_ERROR_1) == (len(cur) - len(LOG_ERROR))) :
			state = 1
		else :
			continue 
		# traverse from success
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
						for k, v in value.items() :
							if k == LOG_EXTRACT_KEY_CHILD :
								if len(sys.argv) == 2 :
									postgres.addLogCookiesDefault(ua_un, json.dumps(v), state)
								else :
									postgres.addLogCookies(ua_un, json.dumps(v), state, json.loads(sys.argv[2]))















