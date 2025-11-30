include $(INC_DIR)/Makefile.inc

REGISTRY_URL = registry.dev.local:9000

# DOCKER_PROXY = m.daocloud.io/docker.io
DOCKER_PROXY := docker.1ms.run

############################################################
# library
############################################################

IMAGE_SRC = $(DOCKER_PROXY)/ubuntu:20.04
IMAGE_DST = $(REGISTRY_URL)/library/ubuntu:20.04
IMAGE = library/ubuntu:20.04

# IMAGE := ubuntu:20.04
# IMAGE := ubuntu:22.04
# IMAGE := ubuntu:24.04
# IMAGE := ubuntu:24.10
# IMAGE := golang:1.22.5
# IMAGE := python:3.12.5
# IMAGE := golang:1.22.5-alpine3.20
# IMAGE := alpine:3.20
# IMAGE := registry:2.8
# IMAGE := joxit/docker-registry-ui:2.5.7
# IMAGE := kindest/node:v1.25.8
# IMAGE := kindest/node:v1.25.16
# IMAGE := kindest/node:v1.27.0
# IMAGE := kindest/node:v1.24.12
# IMAGE := kindest/node:v1.27.0
# IMAGE := redhat/ubi8:8.4
# IMAGE := nginx:1.27.2
# IMAGE := mysql:5.7
# IMAGE := redis:7.0
# IMAGE := cptactionhank/atlassian-confluence:7.9.3
# IMAGE = quay.io/coreos/etcd:v3.4.32 ?
# IMAGE = bitnami/etcd:3.5
# IMAGE = sigoden/dufs:v0.42.0
# IMAGE := mysql:8.0
# IMAGE := python:3.11-slim-bullseye
# IMAGE := python:2.7.18
# IMAGE := golang:1.25.0
# IMAGE := busybox:1.36
# IMAGE := busybox:1.36-glibc

############################################################
# other
############################################################

# IMAGE := b3log/siyuan:v3.0.17

# IMAGE_SRC = $(DOCKER_PROXY)/$(IMAGE)
# IMAGE_DST = $(REGISTRY_URL)/$(IMAGE)

############################################################
# devel build image
############################################################

# IMAGE = devel/ubuntu-22.04-local:latest

############################################################
# command
############################################################

pull-origin:		## download origin image and tag
	docker pull $(IMAGE_SRC)
	@echo
	docker tag $(IMAGE_SRC) $(IMAGE_DST)
	@echo
	docker rmi $(IMAGE_SRC)

po: pull-origin

push: 		## push image to registry
	docker push $(IMAGE_DST)

pull:		## pull image from registry
	docker pull $(IMAGE_DST)

check:		## check registry
	curl http://$(REGISTRY_URL)/v2/_catalog


############################################################
# save
############################################################

DFS_IMAGE_DIR = $(DFS_DIR)/images
SAVE_DIR = ./saves

# 镜像文件名，换所有/为_, 替换所有:为_
IMG_NAME = $(shell echo "$(IMAGE)" | sed 's/\//_/g' | sed 's/:/_/g').img
IMG_TAR = $(IMG_NAME).tar.gz

# 镜像保存路径
IMAGE_SAVE_FILE = $(SAVE_DIR)/$(IMG_NAME)
IMAGE_TAR_FILE = $(SAVE_DIR)/$(IMG_TAR)
IMAGE_UPLOAD_FILE = $(DFS_IMAGE_DIR)/$(IMG_TAR)

desc:
	@echo $(IMG_NAME)
	@echo $(IMG_TAR)

save: 	# save
	@echo "source image: $(IMAGE)"
	@echo "save to:      $(IMAGE_SAVE_FILE)"
	if [ ! -d "$(SAVE_DIR)" ]; then set -x; mkdir -p $(SAVE_DIR); fi
	if [ -f $(IMAGE_SAVE_FILE) ]; then set -x; rm $(IMAGE_SAVE_FILE); fi
	docker save -o ${IMAGE_SAVE_FILE} ${IMAGE_DST}

tar:
	if [ -f $(IMAGE_TAR_FILE) ]; then set -x; rm $(IMAGE_TAR_FILE); fi
	cd $(SAVE_DIR); tar -czvf $(IMG_TAR) $(IMG_NAME)
	rm -f $(IMAGE_SAVE_FILE)
	@echo
	ls -alh $(SAVE_DIR)

upload:
	if [ -f $(IMAGE_UPLOAD_FILE) ]; then set -x; rm $(IMAGE_UPLOAD_FILE); fi	
	cp $(IMAGE_TAR_FILE) $(IMAGE_UPLOAD_FILE)
	@echo
	ls -alh $(IMAGE_UPLOAD_FILE)


############################################################
# load
############################################################

download:
	if [ -f $(IMAGE_TAR_FILE) ]; then set -x; rm $(IMAGE_TAR_FILE); fi
	curl -o $(IMAGE_TAR_FILE) $(DFS_DATA_URL)/images/$(IMG_TAR)
	@echo
	ls -alh $(SAVE_DIR)

untar:
	if [ -f $(IMAGE_SAVE_FILE) ]; then set -x; rm $(IMAGE_SAVE_FILE); fi
	cd $(SAVE_DIR); tar -xzvf $(IMG_TAR)
	rm -f $(IMAGE_TAR_FILE)
	@echo
	ls -alh $(SAVE_DIR)

load:		## load
	docker image rm ${IMAGE_DST}
	docker load -i $(IMAGE_SAVE_FILE) 

clean:
	if [ -f $(IMAGE_SAVE_FILE) ]; then set -x; rm $(IMAGE_SAVE_FILE); fi
	if [ -f $(IMAGE_TAR_FILE) ]; then set -x; rm $(IMAGE_TAR_FILE); fi
	@echo
	ls -alh $(SAVE_DIR)

ls:
	ls -alh $(SAVE_DIR)
	@echo
	du -sh $(SAVE_DIR)
	@echo
	ls $(SAVE_DIR) | wc -l

