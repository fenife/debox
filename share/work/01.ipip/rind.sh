#!/bin/bash

. ./common.sh
. ./netns.sh

# set -x
# echo "argv: $*"
# echo

tcp_cap_peer1_file=/tmp/peer1.pcap
tcp_cap_peer2_file=/tmp/peer2.pcap

function _parse_cap_file {
    tcpdump -nvv -r $tcp_cap_peer1_file
    echo
    tcpdump -nvv -r $tcp_cap_peer2_file
}

function _ping_and_tcpdump() {
    tcpdump -i $veth_peer1 -nvv -U -w $tcp_cap_peer1_file &
    tcpdump -i $veth_peer2 -nvv -U -w $tcp_cap_peer2_file &
    sleep 1
    ping1
    sleep 2
    _stop_program tcpdump
    sleep 1
    echo
    _parse_cap_file
}

function info() {
    conntrack -L  
}

function pd() {
    _ping_and_tcpdump
}

function pr() {
    _parse_cap_file
}

if [[ -z "$1" ]] || [[ $1 == help ]]; then
    help
else
    set -x
    eval $* 
fi

