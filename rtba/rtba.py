#/usr/bin/env python
# -*- coding: UTF-8 -*-  
import sys
import re 
import json
line =  sys.stdin.read()
try:
        ip = re.findall('IP:([^IP:].*)',line) + [""]
        real = re.findall('真人概率：([^真].*%)',line) + [""]
        sj = re.findall('\d{4}-.*',line) + [""]
        xw = re.findall('行为位置:([^行][^\s]*)',line) + [""]
        yy = re.findall('运营商:([^运][^\s]*)',line) + [""]
        ww = re.findall('网络位置: ([^网][^\s]*)',line) + [""]
        ws = re.findall('.*(?= ,真人概率)',line) + [""]
        result = {}
        result['IP'] = ip[0]
        result['真人概率'] = real[0]
        result['时间'] = sj[0]
        result['行为位置'] = xw[0]
        result['运营商'] = yy[0]
        result['网络位置'] = ww[0]
        result['网络属性'] = ws[0]
        print json.dumps(result,ensure_ascii=False,indent=2)
except IndexError:
        print 'something wrong'
        print json.dumps(line,ensure_ascii=False,indent=2)
except Exception, e:
        print 'something wrong'
        print json.dumps(line,ensure_ascii=False,indent=2)
        raise
else:
        pass
finally:
        pass
