
CUR_DIR := $(shell pwd)
PUB_DIR := $(shell readlink -f $(CUR_DIR)/../..)
BASE_DIR := /wine

CONF_DIR = ${HOME}/.config/code-server
SETTING_DIR = ${HOME}/.local/share/code-server/User

PKG_CODER_DIR = ${DFS_DIR}/pkgs/coder
PKG_EXT_DIR = ${DFS_DIR}/pkgs/vscode/ext

help:		## help
	@echo "usage:"
	@echo "  pub dir:       ${PUB_DIR}"
	@echo "  pkg coder dir: ${PKG_CODER_DIR}"
	@echo "  pkg ext dir:   ${PKG_EXT_DIR}"
	@echo "  conf dir:      ${CONF_DIR}"
	@echo "  setting dir:   ${SETTING_DIR}"
	@echo
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s \033[0m%s\n", $$1, $$2}'

h: help		## help

pre:		## prepare
	mkdir -p ${CONF_DIR}
	@echo
	ls -alh ${SETTING_DIR}

cp-conf:		## copy config
	cp ${DFS_DIR}/configs/coder/config.yaml ${CONF_DIR}
	cp ${DFS_DIR}/configs/coder/settings.json ${SETTING_DIR}
	@echo
	ls ${CONF_DIR}
	ls ${SETTING_DIR}

install-dep:		## install dep package
	sudo dpkg -i ${PKG_CODER_DIR}/code-server_4.102.0_amd64.deb

install-rpm:		## install rpm package
	sudo rpm -i ${PKG_CODER_DIR}/code-server_4.102.0_amd64.rpm

enable:		## enable code server
	sudo systemctl enable --now code-server@${USER}

start:		## stop code server
	sudo systemctl start code-server@${USER}

stop:		## stop code server
	sudo systemctl stop code-server@${USER}

restart: stop start		## restart

status:		## status code server
	sudo systemctl status code-server@${USER} | cat

ps: status ## code server ps 
	
