#!/bin/bash
#counter=0
for it in ../logs/*.json;
{ 
       echo $it
       python extractPostLogs.py $it
}
