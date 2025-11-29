include $(INC_DIR)/Makefile.inc

############################################################
# origin
############################################################

# IMAGE := b3log/siyuan:v3.0.17
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
IMAGE := kindest/node:v1.24.12
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

# DOCKER_PROXY = m.daocloud.io/docker.io
DOCKER_PROXY := docker.1ms.run

IMAGE_SRC = $(DOCKER_PROXY)/$(IMAGE)
IMAGE_REG = $(REGISTRY_URL)/$(IMAGE)

############################################################
# devel build image
############################################################

# IMAGE = devel/ubuntu-22.04-local:latest

IMAGE_REG = $(REGISTRY_URL)/$(IMAGE)

############################################################
# command
############################################################

pull-origin:		## download origin image and tag
	docker pull $(IMAGE_SRC)
	@echo
	docker tag $(IMAGE_SRC) $(IMAGE_REG)
	@echo
	docker rmi $(IMAGE_SRC)

push: 		## push image to registry
	docker push $(IMAGE_REG)

pull:		## pull image from registry
	docker pull $(IMAGE_REG)

check:		## check registry
	curl http://$(REGISTRY_URL)/v2/_catalog

po: pull-origin

SAVE_DIR=./saves
# 替换所有/为_, 替换所有:为_
IMAGE_SAVE := $(SAVE_DIR)/$(shell echo "$(IMAGE)" | sed 's/\//_/g' | sed 's/:/_/g').img
IMAGE_TAR := $(IMAGE_SAVE).tar.gz

save: 	# save
	@echo "source image: $(IMAGE)"
	@echo "save to:      $(IMAGE_SAVE)"
	@if [ ! -d "$(SAVE_DIR)" ]; then set -x; mkdir -p $(SAVE_DIR); fi
	@if [ -f $(IMAGE_SAVE) ]; then set -x; rm $(IMAGE_SAVE); fi
	docker save -o ${IMAGE_SAVE} ${IMAGE_REG}
	@if [ -f $(IMAGE_TAR) ]; then set -x; rm $(IMAGE_TAR); fi
	tar -czvf $(IMAGE_TAR) $(IMAGE_SAVE)
	rm -f $(IMAGE_SAVE)
	@echo
	ls -alh $(SAVE_DIR)

load:		## load
	# docker image rm $(IMAGE_SAVE)
	@if [ -f $(IMAGE_SAVE) ]; then set -x; rm $(IMAGE_SAVE); fi
	tar -xzvf $(IMAGE_TAR)
	docker load -i $(IMAGE_SAVE) 
	rm -f $(IMAGE_SAVE)

ls:
	ls -alh $(SAVE_DIR)
	@echo
	du -sh $(SAVE_DIR)
	@echo
	ls $(SAVE_DIR) | wc -l

