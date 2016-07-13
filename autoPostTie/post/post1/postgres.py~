#coding=utf-8

import psycopg2
import psycopg2.extras
import psycopg2.errorcodes
from datetime import datetime


database = "hub"
user = "tieba_login_bot_0"
password = ""
host = "127.0.0.1"
port = "27213"


def updateOperation(sql, param) :
	try :
		conn = psycopg2.connect(database=database, user=user,  password=password, host=host, port=port)
		cursor = conn.cursor()
		cursor.execute(sql, param)
		conn.commit()
		cursor.close()
		conn.close()
	except psycopg2.Error as e :
		print psycopg2.errorcodes.lookup(e.pgcode)


def queryOperation(sql, param = None) :
	try :
		conn = psycopg2.connect(database=database, user=user,  password=password, host=host, port=port)
		cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		if param :
			cursor.execute(sql, param)
		else :
			cursor.execute(sql)
		result = cursor.fetchall()
		cursor.close()
		conn.close()
		return result
	except psycopg2.Error as e :
		print psycopg2.errorcodes.lookup(e.pgcode)

def addLogCookies(un_ua, cookies, state, obj):
	sql = "insert into hub.tieba_login_sessions(username, useragent, cookies, state"
	#print un_ua["un"]
	#print un_ua["ua"]
	param = [un_ua["un"],un_ua["ua"], cookies, state]
	for k, v in obj.items() :
		sql = sql + ", " + k
		param.append(v)
	sql = sql + ") values (%s, %s, %s, %s"
	for i in range(len(obj)) :
		sql = sql + ", %s"
	sql = sql + ");"
	# print sql
	# print obj
	updateOperation(sql, tuple(param))
