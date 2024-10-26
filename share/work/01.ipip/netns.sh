#!/bin/bash

ns1="ns1"
veth1="veth1"
veth_peer1="peer1"
veth1_addr="10.10.1.2/24"
veth1_ip="10.10.1.2"
veth_peer1_addr="10.10.1.1/24"
ns1_subnet="10.10.1.0/24"
ns1_gw="10.10.1.1"
ns1_inner_ip="192.168.1.10"
ns1_tun1="tun1"

ns2="ns2"
veth2="veth2"
veth_peer2="peer2"
veth2_addr="10.10.2.2/24"
veth2_ip="10.10.2.2"
veth_peer2_addr="10.10.2.1/24"
ns2_subnet="10.10.2.0/24"
ns2_gw="10.10.2.1"
ns2_inner_ip="192.168.2.10"
ns2_tun2="tun2"

echo

function ns_setup() {
    # 1、创建两个网络命名空间
    ip netns add ${ns1}
    ip netns add ${ns2}

    # 2、创建两对 veth pair ，一端各挂在一个命名空间下
    ip link add ${veth1} type veth peer name ${veth_peer1}
    ip link add ${veth2} type veth peer name ${veth_peer2}

    ip link set ${veth1} netns ${ns1}
    ip link set ${veth2} netns ${ns2}

    # 3、分别配置地址，并启用
    ip addr add ${veth_peer1_addr} dev ${veth_peer1}
    ip link set ${veth_peer1} up
    ip addr add ${veth_peer2_addr} dev ${veth_peer2}
    ip link set ${veth_peer2} up

    ip netns exec ${ns1} ip addr add ${veth1_addr} dev ${veth1}
    ip netns exec ${ns1} ip link set ${veth1} up
    ip netns exec ${ns2} ip addr add ${veth2_addr} dev ${veth2}
    ip netns exec ${ns2} ip link set ${veth2} up

    # 4、分别配置路由
    ip netns exec ${ns1} route add -net ${ns2_subnet} gw ${ns1_gw}
    ip netns exec ${ns2} route add -net ${ns1_subnet} gw ${ns2_gw}

    # 此时执行ping是通的
    # ip netns exec ${ns1} ping ${veth2_ip} -W1 -c1

    # 5、创建 tun设备，并设置为ipip隧道
    ip netns exec ${ns1} ip tunnel add ${ns1_tun1} mode ipip remote ${veth2_ip} local ${veth1_ip}
    ip netns exec ${ns1} ip link set ${ns1_tun1} up
    ip netns exec ${ns1} ip addr add ${ns1_inner_ip} peer ${ns2_inner_ip} dev ${ns1_tun1}

    ip netns exec ${ns2} ip tunnel add ${ns2_tun2} mode ipip remote ${veth1_ip} local ${veth2_ip}
    ip netns exec ${ns2} ip link set ${ns2_tun2} up
    ip netns exec ${ns2} ip addr add ${ns2_inner_ip} peer ${ns1_inner_ip} dev ${ns2_tun2}
}

function ping1() {
    # 测试隧道是否通
    ip netns exec ${ns1} ping ${ns2_inner_ip} -W1 -c1
}

function ping2() {
    # 测试隧道是否通
    ip netns exec ${ns2} ping ${ns1_inner_ip} -W1 -c1
}

function ns_clear() {
    ip netns del ${ns1}
    ip netns del ${ns2}
}

function _ns_info() {
    ip netns exec $1 ip addr
	echo
	ip netns exec $1 route -n
	# echo
	# ip netns exec $1 netstat -nat
}

function ns1() {
    _ns_info ${ns1}
}

function ns2() {
    _ns_info ${ns2}
}
