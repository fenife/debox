
CUR_DIR := $(shell pwd)
PUB_DIR := $(shell readlink -f $(CUR_DIR)/../..)
BASE_DIR := /wine

REGISTRY_NAME = docker-registry
REGISTRY_IMAGE = ${REGISTRY_URL}/library/registry:2.8
REGISTRY_PORT = 9000
REGISTRY_DATA = ${BASE_DIR}/var/lib/registry

help:
	@echo "usage:"
	@echo "  pub dir:  ${PUB_DIR}"
	@echo "  data dir: ${REGISTRY_DATA}"
	@echo
	@echo "  pre		- 准备 var data 目录"
	@echo "  start		- start registry"
	@echo "  stop		- stop registry"
	@echo "  restart	- restart registry"
	@echo "  check		- check registry"

h: help

pre:	## prepare
	mkdir -p ${REGISTRY_DATA}
	@echo
	ls -alh ${REGISTRY_DATA}

start:	## start registry
	docker run -d --restart unless-stopped \
	--name ${REGISTRY_NAME} \
	-p ${REGISTRY_PORT}:5000 \
	-v ${REGISTRY_DATA}:/var/lib/registry \
	${REGISTRY_IMAGE}

stop:		## stop registry
	docker stop ${REGISTRY_NAME}
	docker rm ${REGISTRY_NAME}

restart: stop start

check:		## check registry
	curl http://${REGISTRY_URL}/v2/_catalog

