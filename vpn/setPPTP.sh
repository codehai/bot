#!/bin/bash
echo "vpnNum"$1
echo "vpnserver"$2
echo "username"$3
echo "password"$4
pptpsetup --create vpn"$1" --server $2 --username $3 --password $4 --encrypt --start
#pptpsetup --create vpn"$1" --server zxfzcd.6655.la --username qa108 --password e468fujl6867 --encrypt --start
echo "set pptp"
localIP=` ip addr | grep "peer" | grep -o 'inet [0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+'`
echo $localIP
#pon vpn"$1"
route add default gw "$localIP" 
curl ip.rtbasia.com
