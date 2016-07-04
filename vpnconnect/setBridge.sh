#!/bin/bash
#入口参数　$1　vpn用户名　$2　vpn密码
set -x
date
#sudo rm /etc/ppp/peers/vpn*
#sudo ip netns exec ns1 ip link del veth1a
Num=$4 #`ip netns list | sed -n "1"p` 
ns=ns"$Num"
veth0=veth"$Num" #veth0
veth1=veth"$Num"a #veth1
br=br"$Num"

ip netns del $ns
brctl delif $br eth0
ifconfig $br down
brctl delbr $br
ip link del $veth0

ip netns add $ns
ip link add $veth0 type veth peer name $veth1
ip link set $veth1 netns $ns
ifconfig $veth0 192.168.6.5/24
ip netns exec $ns ifconfig $veth1 192.168.6.104/24 up
brctl addbr $br
brctl addif $br eth0
brctl addif $br $veth0
#ifconfig eth0 0.0.0.0
ifconfig $veth0 0.0.0.0
dhclient $br
ip netns exec $ns dhclient $veth1
ip netns exec $ns ip addr
ip netns exec $ns ping 114.114.114.114 -c 3
ip netns exec $ns nslookup baidu.com
#ip netns exec $ns ./setPPTP.sh $Num $1 $2 $3 $5
