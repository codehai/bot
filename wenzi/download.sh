#!/bin/bash
let i=0;
while read line
do
{
        let i=i+1; 
        v=`expr $i % 2`;
        if [ $v == 1 ]
        then
			  #echo $v;
			  #echo $i;
			  first=`echo ${line}@`;
			  echo $first
        else
			  second=`echo ${line}@@`;
			  echo $second
        fi
}
done

# while read line
# do 
#     let i=i+1; 
#     echo "File:${line} | cut -f 2 -d " ""
# done < data.dat
