
include ../Makefile.common

CENTOS_IMAGE_FROM=centos:8.4.2105
DEVC_CENTOS_IMAGE=devc-centos-8.4:latest

CENTOS_IMAGE=$(DEVC_CENTOS_IMAGE)
CENTOS_NAME=centos8
CENTOS_DATA_DIR=$(ROOT_DIR)/var/centos8

pull:
	docker pull $(CENTOS_IMAGE)

build: 
	docker build -t $(CENTOS_IMAGE) .

start: 
	docker run $(DEVC_WITH_OPTIONS) \
	--name $(CENTOS_NAME) --hostname $(CENTOS_NAME) \
	-v $(shell pwd)/../dind:/wine/dind \
	$(CENTOS_IMAGE)

stop:
	docker stop $(CENTOS_NAME)
	docker rm $(CENTOS_NAME)

enter:
	docker exec -it $(CENTOS_NAME) zsh


