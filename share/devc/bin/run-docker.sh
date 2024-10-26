#!/bin/bash

# set -x

# PID=`ps -ef | grep "$docker_bin" | grep -v grep | awk '{print $2}'`

# https://docs.docker.com/config/daemon/logs/
PID=`pidof dockerd`

function start {
    if [[ "" ==  "$PID" ]]; then
        dockerd >> /dev/null 2>&1 &
        echo "dockerd start ..."
    else
        echo "dockerd has already started at: $PID"
    fi
}

function stop {
    if [[ "" !=  "$PID" ]]; then
        echo "kill $PID, dockerd stop ..."
        kill -9 $PID
    else
        echo "dockerd not started"
    fi
}

function restart {
    stop
    start
}

function usage {
    echo "usage:"
    echo "  $0 {start|stop|restart}"
}

case "$1" in 
"start") 
    start
    ;;
"stop")
    stop
    ;;
"restart")
    restart
    ;;
"")
    usage
    exit 
    ;;
esac
