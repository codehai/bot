#/usr/bin/env python
#ecoding=utf-8  
import sys
import re 
import json
import postgres
from types import *

line =  sys.stdin.read()
s = ""
t = None
baidu = 0
delRtba = None
logs = json.loads(line)
for log in logs:                  
        if type(log) is DictType:
                delRtba = str(json.dumps(log))
                ip = log['IP'].encode("utf-8")
                if  not ip:
                        ip = None
                real = log[u'真人概率'].encode("utf-8")
                real = (re.findall('\d\d',real) + [''])[0] 
                if real:
                        real = int(real) / 100.0
                else:
                        real = None
                sj = log[u'时间'].encode("utf-8")
                if not sj:
                        sj = None
                xw = log[u'行为位置'].encode("utf-8")
                if not xw:
                        xw = None
                yy = log[u'运营商'].encode("utf-8")
                if not yy:
                        yy = None
                ww = log[u'网络位置'].encode("utf-8")
                if not ww:
                        ww = None
                ws = log[u'网络属性'].encode("utf-8")
                if not ws:
                        ws = None
        else:
                if re.findall('s\d+',log):
                        if s:
                                if delRtba:
                                        postgres.addRtba(s ,t , ip, real, sj, xw, yy, ww, baidu, ws)
                                else:
                                        ip = real = sj = xw = yy = ww = ws =None
                                        postgres.addRtba(s ,t , ip, real, sj, xw, yy, ww, baidu, ws)
                                s = str(re.findall('s\d+',log)[0])
                        else:
                                s = str(re.findall('s\d+',log)[0])   
                if re.findall('Could not resolve host',log):
                        baidu = '1'
                if re.findall('\w{3}\s\w{3}\s.*\d{4}',log):
                        t = str(log)
                if re.findall('something wrong',log):
                        delRtba = ""
                        ip = None
                        real = None
                        sj = None
                        xw = None
                        yy = None
                        ww = None
                        ws = None
if delRtba:
        postgres.addRtba(s ,t , ip, real, sj, xw, yy, ww, baidu, ws)
else:
        ip = real = sj = xw = yy = ww = ws= None
        postgres.addRtba(s ,t , ip, real, sj, xw, yy, ww, baidu, ws)

