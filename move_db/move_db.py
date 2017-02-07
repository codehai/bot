#coding=utf-8
import re
import sys
import sqlite3
import csv
import psycopg2
import psycopg2.extras
import psycopg2.errorcodes
 
database = ""
user = ""
password = ""
host = ""
port = ""
 
def select_table():
    conn = sqlite3.connect('/path/db.sqlite3',timeout=30.0)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return tables
 
def backup_table(table):
    conn = sqlite3.connect('/path/db.sqlite3',timeout=30.0)
    cursor = conn.cursor()
    sql = "PRAGMA table_info(%s)" %(table)
    cursor.execute(sql)
    col_names = cursor.fetchall()
    #print(col_names)
    name_list = ''
    for col_name in col_names:
        name_list = name_list + col_name[1]
        if not col_name == col_names[-1]:
            name_list = name_list + ','
    #print(name_list)
    sql = 'select %s from %s' %(name_list,table)
    csvfile = '/tmp/%s.csv' %(table)
    data = cursor.execute(sql)
 
    with open(csvfile, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)
def up_postgres(table):
    try:
        conn = psycopg2.connect(database=database, user=user,  password=password, host=host, port=port)
        cursor = conn.cursor()
        sql = 'TRUNCATE TABLE  %s CASCADE;' %(table)
        cursor.execute(sql)
        sql = "COPY %s FROM '/tmp/%s.csv' DELIMITER ',' CSV;" %(table, table)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except psycopg2.Error as e :
        print(e)
 
if __name__ == "__main__":
    tables = select_table()
    for table in tables:
        if 'races' in table[0]:
            continue
        print(table[0])
        backup_table(table[0])
        up_postgres(table[0])
