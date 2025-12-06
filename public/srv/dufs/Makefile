# see: https://github.com/sigoden/dufs

CUR_DIR := $(shell pwd)
PUB_DIR := $(shell readlink -f $(CUR_DIR)/../..)

DUFS_IMAGE = $(REGISTRY_URL)/sigoden/dufs:v0.42.0
DUFS_NAME = dufs-0.42
DUFS_PORT = 9060
DUFS_DATA = ${PUB_DIR}/var/dfs

help:
	@echo "usage:"
	@echo "  pub dir:  ${PUB_DIR}"
	@echo "  data dir: ${DUFS_DATA}"
	@echo
	@echo "  pre		- 准备 var data 目录"
	@echo "  start		- start dufs"
	@echo "  stop		- stop dufs"
	@echo "  restart	- restart dufs"

h: help

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

restart: stop start


