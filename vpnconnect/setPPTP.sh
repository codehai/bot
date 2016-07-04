#!/bin/bash
set -x
ip addr
route
pptpsetup --create vpn"$1" --server $2 --username $3 --password $4 --encrypt --start
ip addr
route
localIP=`ip addr | tee /dev/stderr | grep "peer" | grep -o 'inet [0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+'`
#if [$localIP]
	#echo $localIP
	#pon vpn"$1"
	route add default gw "$localIP" 
	route
	#curl ip.rtbasia.com
	bash -c $5
#fi
