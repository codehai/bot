#/usr/bin/env python
#coding=utf-8  
import sys
import re 
import json

line =  sys.stdin.read()
tieba = json.loads(line)
output = open('city.txt', 'w+')
print len(tieba[u'地区'])
for sheng in tieba[u'地区']:
        for city in tieba[u'地区'][sheng]:
                print city
                output.write(city.encode("utf-8")+'\n')
                # print json.dumps(tieba[u'地区'][sheng],ensure_ascii=False,indent=2)