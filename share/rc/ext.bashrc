
############################################################
# dirs
BASE_DIR=/wine/debox
BUILD_DIR=/wine/debox/build
ICODE_DIR=/wine/debox/icode
LOCAL_DIR=/wine/debox/local
STG_DIR=/wine/debox/stg
SHARE_DIR=/wine/debox/share

APP_DIR=$SHARE_DIR/app
INC_DIR=$SHARE_DIR/inc
K8S_DIR=$SHARE_DIR/k8s

############################################################
# jump 
alias jbox="cd $BASE_DIR" 
alias jbuild="cd $BUILD_DIR" 
alias jlocal="cd $LOCAL_DIR" 
alias jshare="cd $SHARE_DIR" 
alias japp="cd $APP_DIR" 
alias jk8s="cd $K8S_DIR" 
alias jicode="cd $ICODE_DIR" 

############################################################
# export
export TERM xterm
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

export INC_DIR=$INC_DIR

export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/go/bin:${HOME}/.local/bin:${HOME}/go/bin:${SHARE_DIR}/bin

############################################################
# alias
alias dps="docker ps -a --format 'table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'"
alias dls="docker image ls"

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

