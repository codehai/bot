#coding=utf-8

from datetime import date
import time
from random import choice
import postgres
import json
import sys
import types
import re
import pdb


REG_MAX_FLOOR = "Max Floor(\d+)"
REG_TARGET_FLOOR = "Target Floor(\d+)"
FIND_FLOOR_SUCCESS = "find target floor"
POST_USER = "user:"

POST_SUCCESS = u"回贴成功！"
POST_ERROR_1 = u"您的帐号可能存在不当操作，暂无法正常发贴，您可申请一键恢复"
POST_ERROR_2 = u"发贴含有不适当内容或广告,请重新提交"
POST_ERROR_3 = u"未知错误"
POST_ERROR_4 = u"验证码输入错误,请重新输入"

POST_ERROR_5 = u"无法访问"
POST_ERROR_6 = u"未登录成功，没有查询到用户"
POST_ERROR_7 = 'Traceback (most recent call last):'

logFile = open(sys.argv[1])
jsonStr = logFile.read()
# testFile = open("testFile", 'w')
# testFile.write(jsonStr)
# testFile.close()
jsonObject = json.loads(jsonStr)
logFile.close()

# more = json.loads(len(sys.argv)>2?sys.argv[2]:"{}");
if len(sys.argv)>2:
	more = json.loads(sys.argv[2])
else:
	more = json.loads("{}")

# print "jsonObject: " + str(len(jsonObject)) 
postUser = ""
i = 0
if len(jsonObject)!=1:	
	while i < len(jsonObject) :
		cur = jsonObject[i]
		if isinstance(cur, unicode) :			
			if cur.find(POST_USER) == 0 :
				postUser = re.findall(':([^:]*)',cur)
			elif cur.find(POST_ERROR_5) == 0:
				postgres.addPostedErr('5', POST_ERROR_5, more)
				break
			elif cur.find(POST_ERROR_6) == 0:
				postgres.addPostedErr('6', POST_ERROR_6, more)
				break
			elif cur.find(POST_ERROR_7) == 0:							# 			errorMessage = jsonObject[j] + jsonObject[j+1] +jsonObject[j+2]
				errorMessage = jsonObject[i] + jsonObject[i+1] +jsonObject[i+2]
				errorCodes = re.findall('\d+',jsonObject[i+1])[0]
				if re.findall('driver\.get',jsonObject[i+2]):
					errorCodes = jsonObject[i+2]
					postgres.addPostedErr(7, errorMessage, more)
				elif re.findall('link\_text\("我"\)',jsonObject[i+2]):
					errorCodes = jsonObject[i+2]
					postgres.addPostedErr(8, errorMessage, more)
				elif re.findall('css\_selector\(".blue\_kit\_left',jsonObject[i+2]):
					errorCodes = jsonObject[i+2]
					postgres.addPostedErr(10, errorMessage, more)
				elif re.findall('By\.TAG\_NAME,\'input\'',jsonObject[i+2]):
					errorCodes = jsonObject[i+2]
					postgres.addPostedErr(11, errorMessage, more)
				elif re.findall('move\_to\_element\(btn\)',jsonObject[i+2]):
					errorCodes = jsonObject[i+2]
					postgres.addPostedErr(12, errorMessage, more)
				elif re.findall('driver\.add\_cookie',jsonObject[i+2]):
					errorCodes = jsonObject[i+2]
					postgres.addPostedErr(13, errorMessage, more)
				else:
					postgres.addPostedErr(errorCodes, errorMessage, more)
				break	
		if isinstance(cur,dict):
			if cur.has_key('content'):
				findNext = False
				findLast = False
				status = 0
				tie = jsonObject[i]
				for j in range(i,len(jsonObject)):
					if isinstance(jsonObject[j],list):
						findNext = True
						break
				for k in range(i, 0, -1):
					if isinstance(jsonObject[k],list):
						findLast = True
					elif isinstance(jsonObject[k], unicode):
						targetMatch = re.match(REG_TARGET_FLOOR, jsonObject[k])
						if jsonObject[k] == POST_SUCCESS :
							status = 200
						elif jsonObject[j] == POST_ERROR_1 :
							status = 1
						elif jsonObject[j] == POST_ERROR_2:
							status = 2
						elif jsonObject[j] == POST_ERROR_3:
							status = 3
						elif jsonObject[j] == POST_ERROR_4:
							status = 4
						elif targetMatch:
							target = targetMatch.group(1) 
							break
				if findNext and findLast:
					fenxi = 1
				else:
					fenxi = 0
				tiezi = json.dumps(tie,ensure_ascii=False).replace('\u0000','')
				postgres.addPostedTie(postUser[0], target, tiezi, status, fenxi, more)
	
		i = i + 1
else:
	postgres.addPostedErr(0, 'null', more)	