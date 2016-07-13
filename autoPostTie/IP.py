#coding=utf-8
import re
import codecs
import psycopg2
conn = psycopg2.connect(database="dev", user="tiebabot0", password="y53bnd573w4r", host="123.59.77.204", port="27213")
data = open('IPDatas.txt')
cur = conn.cursor()
for each_line in data:    
        match = re.findall(r'\S+',each_line)
        for ip in match:
            print(ip.decode('gbk'))
            #cur.execute("INSERT INTO IP (startIP,endIP,Contry,Local) VALUES (1, 'Paul', 32, 'California', 20000.00 )")
             