#!/bin/bash
while read line
do 
    echo "${line}"
    python checkPostedTie.py
done < case1.txt