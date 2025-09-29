
# usage:
# export INC_DIR=/wine/devbox/share/include
# include $(INC_DIR)/Makefile.common


.PHONY: build start stop run pull at attach enter exec sys rund startd

############################################################
# env
############################################################

BASE_DIR=/wine/debox
BUILD_DIR=$(BASE_DIR)/build
IMAGE_SAVE_DIR=$(BASE_DIR)/images
ICODE_DIR=$(BASE_DIR)/icode
SHARE_DIR=$(BASE_DIR)/share

VENV_DIR=/wine/venv

INC_DIR=$(SHARE_DIR)/inc
INC_SH_DIR=$(INC_DIR)/sh

# 执行的makefile文件
EXEC_MAKEFILE = $(abspath $(firstword $(MAKEFILE_LIST)))
# 执行的makefile路径
EXEC_MAKEFILE_PATH = $(dir $(EXEC_MAKEFILE))
# 执行的makefile所在的文件夹
EXEC_DIR = $(shell basename $(EXEC_MAKEFILE_PATH))

FILE_SERVER_URL = stg-fileserver.me:8800
REGISTRY_URL = registry.me:9000

IMAGE_ME_NS = $(REGISTRY_URL)/fenife

# time
NOW = $(shell date '+%Y-%m-%d %H:%M:%S')
NOW_TS = $(shell date '+%s')

# ETH_NAME=ens33
ETH_NAME=$(shell ifconfig -s | grep -E 'eth|ens|enp' | grep -v 'veth' | awk '{print $$1}')
HOST_IP=$(shell ifconfig | grep $(ETH_NAME) -A 2 | grep inet | head -1 | awk '{print $$2}')
# HOST_IP=192.168.0.2
HOST_NAME=$(shell hostname)

DEVC_WITH_OPTIONS = --rm -it --privileged \
	--add-host="dev.local:$(HOST_IP)"  \
	-v $(SHARE_DIR):$(SHARE_DIR) \
	-v $(ICODE_DIR):$(ICODE_DIR) 

############################################################
# help
############################################################

common: 	## --------------------------------------------- 

help: 	## print help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s \033[0m%s\n", $$1, $$2}'

cmd:	## print commands
	@LC_ALL=C $(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | grep -E -v -e '^[^[:alnum:]]' -e '^$@$$'

sys: ## print system info
	@echo "-------------------- time info --------------------"
	@echo "now:     $(NOW)"
	@echo "ts:      $(NOW_TS)"
	@echo
	@echo "-------------------- path info --------------------"
	@echo "exec makefile:        $(EXEC_MAKEFILE)"
	@echo "exec makefile path:   $(EXEC_MAKEFILE_PATH)"
	@echo "exec dir:             $(EXEC_DIR)"
	@echo
	@echo "-------------------- system info --------------------"
	-cat /etc/os-release
	@echo
	-cat /etc/lsb-release
	@echo
	cat /proc/version
	@echo
	uname -r
	@echo
	@echo "eth name:  $(ETH_NAME)"
	@echo "host ip:   $(HOST_IP)"
	@echo "host name: $(HOST_NAME)"
	@echo

############################################################
# alias 
############################################################
run: start		## run/start
rund: startd	## run/start daemon
at: enter		## attach to container
attach: enter	## attach to container
exec: enter		## attach to container
st: status		## status

############################################################
# cmd
############################################################
prune:	## docker image prune
	docker image prune


############################################################
# images
############################################################

# 保存镜像
# $1: docker image name
define _save_image
	$(INC_SH_DIR)/image.sh save $(1)
endef

# $1: docker image name
define _load_image
	$(INC_SH_DIR)/image.sh load $(1)
endef
