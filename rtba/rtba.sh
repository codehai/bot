 #!/bin/bash
 value=$(cat)
IP=`$value | grep -o "IP:[0-9]*.[0-9]*.[0-9]*.\w\+"  | cut -f 2 -d ":"`
SHIJIAN=`$value | grep -o "[0-9]\{4\}-.*+[0-9]\{4\}"`
GAILV=`$value | grep -o "真人概率：\w\+%"  | grep -o "[0-9]\{2\}%"`
XWEIZHI=`$value | grep -o "行为位置:.*\s" | cut -f 2 -d ":" | cut -f 1 -d " "` 
YUNYING=`$value | grep -o "运营商:.*" | cut -f 2 -d ":" ` 
WWEIZHI=`$value | grep  -o "网络位置: \[.*\.[0-9]\+)" | cut -f 2 -d ":"`

IP1=`$value | grep -o "IP:[0-9]*.[0-9]*.[0-9]*.\w\+" ` 
SHIJIAN1=`$value | grep -o "[0-9]\{4\}-.*+[0-9]\{4\}"`
GAILV1=`$value | grep -o "真人概率：\w\+%" `
XWEIZHI1=`$value | grep -o "行为位置:.*\s" ` 
YUNYING1=`$value | grep -o "运营商:.*" ` 
WWEIZHI1=`$value | grep  -o "网络位置: \[.*\.[0-9]\+)"`

 CONTENT = `$value | sed -s 's/^.*[^0-9]\([0-9]\+\).*[^A-Z]\([A-Z]\+\).*$/number:\1\nCAPITAL:\2/' ` 

echo $CONTENT

 echo $IP1
 echo $SHIJIAN1
 echo $GAILV1
 echo $XWEIZHI1
 echo $YUNYING1
 echo $WWEIZHI1

echo  {\"IP\":\"$IP\", \"时间\":\"$SHIJIAN\", \"真人概率\":\"$GAILV\", \"行为位置\":\"$XWEIZHI\",\"运营商\":\"$YUNYING\",\"网络位置\":\"$WWEIZHI\"} | jq .
