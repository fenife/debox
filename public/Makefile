
CUR_DIR := $(shell pwd)
# PUB_DIR := $(shell readlink -f $(CUR_DIR)/../..)
PUB_ETC_DIR=$(CUR_DIR)/etc
PUB_VAR_DIR=$(CUR_DIR)/var
BASE_DIR=/wine

help:	## help
	@echo "usage:"
	@echo "  pub dir:       ${PUB_DIR}"
	@echo "  etc dir:       ${PUB_ETC_DIR}"
	@echo "  pub var dir:   ${PUB_VAR_DIR}"
	@echo "  base dir:      ${BASE_DIR}"
	@echo
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s \033[0m%s\n", $$1, $$2}'

h: help		## help

pre:		## pre
	if [ -f $(PUB_VAR_DIR) ]; then set -x; rm $(PUB_VAR_DIR); fi
	@echo
	if [ -f $(BASE_DIR) ]; then set -x; rm $(BASE_DIR); fi

cat-hosts:	## cat pub etc hosts
	cat ${PUB_ETC_DIR}/hosts

set-hosts:	## setup hosts
	@echo "======================================================"
	@echo "添加 hosts: ${PUB_ETC_DIR}/hosts -> /etc/hosts"
	@echo "======================================================"
	cat ${PUB_ETC_DIR}/hosts | sudo tee -a /etc/hosts
	@echo
	cat /etc/hosts
	
cat-envs:	## cat envs
	cat ${PUB_ETC_DIR}/envs

set-envs-bash:	## setup bashrc
	cat ${PUB_ETC_DIR}/envs | tee -a ~/.bashrc

set-envs-zsh:		## setup zshrc
	cat ${PUB_ETC_DIR}/envs | tee -a ~/.zshrc

