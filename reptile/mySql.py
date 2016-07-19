#coding=utf-8

import pymysql
import pymysql.cursors
import pymysql.err

# Connect to the database

host='localhost'
user='user'
password='passwd'
db='db'
charset='utf8mb4'
cursorclass=pymysql.cursors.DictCursor

def updateOperation(sql, param) :
        try:
                connection = pymysql.connect(host=host,user=user,password=password,db=db,charset=charset,cursorclass=cursorclass)
                with connection.cursor() as cursor:
                        # Create a new record
                        # sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                        # cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
                        cursor.execute(sql, param)
                connection.commit()
                connection.close()
        except pymysql.MySQLError as e:
                print('Got error {!r}, errno is {}'.format(e, e.args[0]))

def addRace(rank, releaseTime, owner, returnTime, speed, distance, company, pigeonID, shedNum, raceName):
        updateOperation("INSERT INTO `race` (`rank`, `releaseTime`, `owner`, `returnTime`, `speed`, `distance`, `company`,  `pigeonID`, `shedNum`, `raceName`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ( rank, releaseTime, owner, returnTime, speed, distance, company, pigeonID, shedNum, raceName))
