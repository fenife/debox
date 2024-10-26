#!/bin/bash


now_dt=`date '+%Y-%m-%d %H:%M:%S'`
now_ts=`date '+%s'`
eth_name=`ifconfig -s | grep -E 'eth|ens' | grep -v 'veth' | awk '{print $1}'`
host_ip=`ifconfig | grep $eth_name -A 2 | grep inet | head -1 | awk '{print $2}'`
host_name=`hostname`

# run and echo commands
function rune(){
    set -x
    # printf "%s " $@
    echo "$@"
    # eval $@
}


function help() {
    echo "------------------------------"
    echo "usage:"

    IFS=$'\n'
    for f in $(declare -F); do
        # 打印函数名, 下划线_开头的函数除外
        # $f: declare -f my_func1, index从0开始, 取11之后的字符, 即函数名
        fn=${f:11}
        if [[ $fn != _* ]];
        then
            echo "  $fn" 
        fi
        # 执行函数
        # eval "$fn"
    done 
}

function _stop_program() {
    PID=`ps -ef | grep "$1" | grep -v grep | awk '{print $2}'`
    kill -SIGINT $PID
}

function sys() {
    set +x
    echo "-------------------- time info --------------------"
	echo "now:     $now_dt"
	echo "ts:      $now_ts"
    echo
	echo "-------------------- host info --------------------"
	echo "eth name:  $eth_name"
	echo "host ip:   $host_ip"
	echo "host name: ${host_name}"
	echo
	echo "-------------------- version info --------------------"
	(set -x; cat /etc/centos-release); echo
	(set -x; cat /proc/version); echo
    (set -x; uname -r); echo

    # set -x
    # ifconfig -s | grep -E 'eth|ens' | grep -v 'veth' | awk '{print $1}'
    # rune ifconfig -s \| grep -E 'eth|ens'
}
