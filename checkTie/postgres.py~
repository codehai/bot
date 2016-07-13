#coding=utf-8

import psycopg2
import psycopg2.extras
import psycopg2.errorcodes
from datetime import datetime


database = "dev"
user = "chatengine0"
password = "sry345edfh22"
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

def addRevisitedTie(tie, log, dead, img):
	updateOperation("insert into posted_tie_revisit (tie, t, log, dead, img) values (%s, %s, %s, %s, %s);", (tie, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), log, dead, img))
