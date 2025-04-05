
# Incremental completion on zsh: 实时补全
# source $ZSH_CUSTOM/plugins/incr/incr.zsh

# 关闭自动更新
zstyle ':omz:update' mode disabled

# 解决zsh粘贴卡慢问题
pasteinit() {
  OLD_SELF_INSERT=${${(s.:.)widgets[self-insert]}[2,3]}
  zle -N self-insert url-quote-magic # I wonder if you'd need `.url-quote-magic`?
}

pastefinish() {
  zle -N self-insert $OLD_SELF_INSERT
}
zstyle :bracketed-paste-magic paste-init pasteinit
zstyle :bracketed-paste-magic paste-finish pastefinish

############################################################
# dirs
BASE_DIR=/wine/debox
BUILD_DIR=$BASE_DIR/build
LOCAL_DIR=$BASE_DIR/local

SHARE_DIR=$BASE_DIR/share
DEVC_DIR=$SHARE_DIR/devc
INC_DIR=$SHARE_DIR/inc
ROAM_DIR=$SHARE_DIR/roam
WORK_DIR=$SHARE_DIR/work
K8S_DIR=$SHARE_DIR/k8s

ICODE_DIR=$BASE_DIR/icode

############################################################
# jump 
alias jbase="cd $BASE_DIR" 
alias jbuild="cd $BUILD_DIR" 
alias jlocal="cd $LOCAL_DIR" 
alias jshare="cd $SHARE_DIR" 
alias jdevc="cd $DEVC_DIR" 
alias jroam="cd $ROAM_DIR" 
alias jwork="cd $WORK_DIR" 
alias jk8s="cd $K8S_DIR" 
alias jicode="cd $ICODE_DIR" 

############################################################
# export
export TERM xterm
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

export INC_DIR=$INC_DIR

export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/go/bin:${HOME}/.local/bin:${HOME}/go/bin

############################################################
# alias

alias kc="kubectl"
alias dps="docker ps -a --format 'table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'"
alias dls="docker image ls"

############################################################

alias runc="make -f Makefile.runc" 
alias runs="make -f Makefile.runs"

alias rinh="make -f Makefile.rinh"
alias rinc="make -f Makefile.rinc"
alias rind="make -f Makefile.rind"
alias rinv="make -f Makefile.rinv"

############################################################
# k8s
if [ -x "$(command -v kubectl)" ]; then
  source <(kubectl completion zsh)
fi

############################################################
# venv
VENV_DIR=/wine/venv

alias sicode="source ${VENV_DIR}/icode/bin/activate"


