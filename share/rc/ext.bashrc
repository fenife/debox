
############################################################
# dirs
############################################################
BASE_DIR=/wine
DEBOX_DIR=${BASE_DIR}/debox

ICODE_DIR=${DEBOX_DIR}/icode
IMAGE_DIR=${DEBOX_DIR}/image
LOCAL_DIR=${DEBOX_DIR}/local
SHARE_DIR=${DEBOX_DIR}/share
PUB_DIR=${DEBOX_DIR}/public

APP_DIR=${SHARE_DIR}/app
INC_DIR=${SHARE_DIR}/inc

DFS_DIR=${DEBOX_DIR}/var/dfs/files

############################################################
# jump 
############################################################
alias jdebox="cd ${DEBOX_DIR}" 

alias jicode="cd ${ICODE_DIR}" 
alias jimage="cd ${IMAGE_DIR}" 
# alias jlocal="cd ${LOCAL_DIR}"
alias jshare="cd ${SHARE_DIR}" 
alias jpub="cd ${PUB_DIR}"

alias jhub="cd ${IMAGE_DIR}/hub"

alias japp="cd ${APP_DIR}" 
alias jk8s="cd ${SHARE_DIR}/k8s" 
alias jsetup="cd ${SHARE_DIR}/setup"

alias jsrv="cd ${PUB_DIR}/srv"
alias jinfra="cd ${PUB_DIR}/infra"
alias jdfs="cd ${DFS_DIR}"

############################################################
# export
############################################################
export TERM xterm
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

## user define envs ##
export BASE_DIR=${BASE_DIR}
export INC_DIR=${INC_DIR}
export DFS_DIR=${DFS_DIR}

export REGISTRY_URL=local.registry.io:9000
export DFS_PUB_URL=http://192.168.200.20:9060/files
export DFS_PRIV_URL=http://192.168.200.20:9060/files

export PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin
export PATH=$PATH:${HOME}/.local/bin:${SHARE_DIR}/bin

export GOPATH=$HOME/go
export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin

export PYTHONPATH=$PYTHONPATH:$ICODE_DIR

# python etcd
export ETCDCTL_API=3
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

############################################################
# alias
############################################################
alias dps="docker ps -a --format 'table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'"
alias dls="docker image ls"
alias dlt="docker image ls | sort -nr"

############################################################
# alias for Makefile
alias runc="make -f Makefile.runc" 
alias runs="make -f Makefile.runs"

alias rinh="make -f Makefile.rinh"
alias rinc="make -f Makefile.rinc"
alias rind="make -f Makefile.rind"
alias rinv="make -f Makefile.rinv"

############################################################
# k8s
alias kc="kubectl"

if [ -x "$(command -v kubectl)" ]; then
  source <(kubectl completion zsh)
fi

############################################################
# venv
VENV_DIR=/wine/venv

alias sicode="source $VENV_DIR/icode/bin/activate"

############################################################
# run service
alias rswebox="make -f ${APP_DIR}/webox/Makefile"

