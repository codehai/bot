#!/bin/bash
for log in ./logs/*.log
do
        httpok=`cat $log | grep -c "HTTP/1.1 200 OK"` || ""
        if [ "$httpok" = "" ];then
                echo $log
        elif [ "$httpok" = "1" ]
        then
                echo $log
        fi
done