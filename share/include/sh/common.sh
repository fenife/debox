#!/bin/bash

ROOT_DIR=/wine
OPT_DIR=/wine/devbox/opt
IMAGE_BUILD_DIR=/wine/devbox/build
IMAGE_SAVE_DIR=/wine/devbox/images

NOW_DT=`date '+%Y-%m-%d %H:%M:%S'`
NOW_TS=`date '+%s'`
ETH_NAME=`ifconfig -s | grep -E 'eth|ens' | grep -v 'veth' | awk '{print $1}'`
HOST_IP=`ifconfig | grep $ETH_NAME -A 2 | grep inet | head -1 | awk '{print $2}'`
HOST_NAME=`hostname`

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
	echo "now:     ${NOW_DT}"
	echo "ts:      ${NOW_TS}"
    echo
	echo "-------------------- host info --------------------"
	echo "eth name:  ${ETH_NAME}"
	echo "host ip:   ${HOST_IP}"
	echo "host name: ${HOST_NAME}"
	echo
	echo "-------------------- version info --------------------"
	(set -x; cat /etc/centos-release); echo
	(set -x; cat /proc/version); echo
    (set -x; uname -r); echo

    # set -x
    # ifconfig -s | grep -E 'eth|ens' | grep -v 'veth' | awk '{print $1}'
    # rune ifconfig -s \| grep -E 'eth|ens'
}

# if [[ -z "$1" ]] || [[ $1 == help ]]; then
#     help
# else
#     set -x
#     eval $* 
# fi

