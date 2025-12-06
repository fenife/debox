
CUR_DIR := $(shell pwd)
# PUB_DIR := $(shell readlink -f $(CUR_DIR)/../..)
PUB_VAR_DIR=$(CUR_DIR)/var

help:
	@echo "usage:"
	@echo "  pub dir: ${PUB_DIR}"
	@echo "  var dir: ${PUB_VAR_DIR}"
	@echo "  pre-var-di 	- 准备./var目录"

pre-var-dir:
	mkdir -p ${PUB_VAR_DIR}/dfs/files
	mkdir -p ${PUB_VAR_DIR}/dfs/files/configs
	mkdir -p ${PUB_VAR_DIR}/dfs/files/images
	mkdir -p ${PUB_VAR_DIR}/dfs/files/pkgs

