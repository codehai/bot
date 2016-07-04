#coding=utf-8

import psycopg2
import psycopg2.extras
import psycopg2.errorcodes
from datetime import datetime


database = "dev"
user = "tiebabot0"
password = "y53bnd573w4r"
host = "123.59.77.204"
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


def addRtba(s ,t , ip, real, sj, xw, yy, ww, baidu, ws):
	updateOperation("insert into rtba (s, 时间1, ip, 真人概率, 时间2, 行为位置, 运营商,  网络位置, baidu, 网络属性) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", ( s , t , ip, real, sj , xw, yy, ww, baidu, ws))

