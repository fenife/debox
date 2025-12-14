# see: https://github.com/sigoden/dufs

CUR_DIR := $(shell pwd)
PUB_DIR := $(shell readlink -f $(CUR_DIR)/../..)

DUFS_IMAGE = $(REGISTRY_URL)/sigoden/dufs:v0.42.0
DUFS_NAME = dufs-0.42
DUFS_PORT = 9060
# dfs 里有部分配置文件是要编辑的，放当前目录下
DUFS_DATA = ${PUB_DIR}/var/dfs

help:		## help
	@echo "usage:"
	@echo "  pub dir:  ${PUB_DIR}"
	@echo "  data dir: ${DUFS_DATA}"
	@echo
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s \033[0m%s\n", $$1, $$2}'

h: help		## help

pre:	## prepare
	mkdir -p ${DUFS_DATA}/files
	mkdir -p ${DUFS_DATA}/files/configs
	mkdir -p ${DUFS_DATA}/files/images
	mkdir -p ${DUFS_DATA}/files/pkgs
	@echo
	ls -alh ${DUFS_DATA}/files


start:	## start dufs
	docker run -d --restart always \
	--name $(DUFS_NAME) \
	-p $(DUFS_PORT):5000 \
	-v $(DUFS_DATA):/data \
	-e DUFS_ALLOW_ALL=false \
	-e DUFS_ALLOW_ARCHIVE=true \
	-e DUFS_ALLOW_SEARCH=true \
	$(DUFS_IMAGE) \
	/data 

stop:		## stop dufs
	docker stop $(DUFS_NAME)
	docker rm $(DUFS_NAME)

restart: stop start		## restart


