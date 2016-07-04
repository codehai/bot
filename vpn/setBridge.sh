#!/bin/bash
#入口参数　$1　vpn用户名　$2　vpn密码
sudo rm /etc/ppp/peers/vpn*
sudo ip netns exec ns1 ip link del veth1a
sudo ip netns del ns1
sudo brctl delif br1 eth0
sudo ifconfig br1 down
sudo brctl delbr br1
Num=$4 #`ip netns list | sed -n "1"p` 
ns=ns"$Num"
echo $ns
veth0=veth"$Num" #veth0
echo $veth0
veth1=veth"$Num"a #veth1
echo $veth1
br=br"$Num"
echo $br
sudo ip netns add $ns
echo "add success"
sudo ip link add $veth0 type veth peer name $veth1
echo "link veth0 to veth1 success"
sudo ip link set $veth1 netns $ns
echo "link veth1 to ns success"
sudo ifconfig $veth0 192.168.5.5/24
echo "set ip success"
sudo ip netns exec $ns ifconfig $veth1 192.168.5.104/24 up
echo "set ip up"
sudo brctl addbr $br
echo "add br"
sudo brctl addif $br eth0
echo "add br to eth0"
sudo brctl addif $br $veth0
echo "add br to veth0"
sudo ifconfig eth0 0.0.0.0
echo "set ip eth0"
sudo ifconfig $veth0 0.0.0.0
echo "set ip veth"
sudo dhclient $br
echo "set client br"
sudo ip netns exec $ns dhclient $veth1
echo "set ns1 clinet veth1"
sudo ip netns exec $ns ./setPPTP.sh $Num $1 $2 $3
