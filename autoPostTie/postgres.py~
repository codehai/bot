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


def addRtba(t, s, log):
	updateOperation("insert into rtba (t, s, log) values (%s, %s, %s);", (q, a, log))

def add(q, a):
	updateOperation("insert into qa (q, a, t) values (%s, %s, %s);", (q, a, datetime.now()))


def findAll() :
	return queryOperation("select * from qa;")

def findByQandA(q, a) :
	return queryOperation("select * from qa where q = %s and a = %s;", (q, a))

def findByQ(q) :
	return queryOperation("select * from qa where q = %s", (q,))

def findByA(a) :
	return queryOperation("select * from qa where a = %s", (a,))

def getQACount() :
	obj = queryOperation("select count(*) from qa");
	return obj[0]['count']

def getFreqA(count) :
	return queryOperation("select a,cnt from (select a,count(*) as cnt from qa group by a) as foo where cnt > %s order by cnt DESC;", (count,))
	
def findTieba(offset, limit = 1000) :
	return queryOperation("select * from tieba order by ba limit %s offset %s", (limit, offset))

def getTiebaCount() :
	obj = queryOperation("select count(*) from tieba");
	return obj[0]['count']

def findCookie(id) :
	return queryOperation("select * from login_cookie where id = %s", (id,))
