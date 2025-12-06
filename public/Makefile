
CUR_DIR := $(shell pwd)
# PUB_DIR := $(shell readlink -f $(CUR_DIR)/../..)
PUB_VAR_DIR=$(CUR_DIR)/var
PUB_ETC_DIR=$(CUR_DIR)/etc

help:
	@echo "usage:"
	@echo "  pub dir: ${PUB_DIR}"
	@echo "  var dir: ${PUB_VAR_DIR}"
	@echo "  etc dir: ${PUB_ETC_DIR}"
	@echo
	@echo "  pre			- 准备./var目录"
	@echo "  cat-hosts		- 查看要添加的 hosts"
	@echo "  set-hosts		- 添加 hosts"
	@echo "  cat-envs		- 查看要添加的 envs"
	@echo "  set-envs-bash	- 添加 envs 到 bashrc"
	@echo "  set-envs-zsh	- 添加 envs 到 zshrc"

h: help

pre:
	mkdir -p ${PUB_VAR_DIR}

cat-hosts:
	cat ${PUB_ETC_DIR}/hosts

set-hosts:
	@echo "======================================================"
	@echo "添加 hosts: ${PUB_ETC_DIR}/hosts -> /etc/hosts"
	@echo "======================================================"
	cat ${PUB_ETC_DIR}/hosts | sudo tee -a /etc/hosts
	@echo
	cat /etc/hosts
	
cat-envs:
	cat ${PUB_ETC_DIR}/envs

set-envs-bash:
	cat ${PUB_ETC_DIR}/envs | tee -a ~/.bashrc

set-envs-zsh:
	cat ${PUB_ETC_DIR}/envs | tee -a ~/.zshrc

