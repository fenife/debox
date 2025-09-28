include $(INC_DIR)/Makefile.inc

# IMAGE := b3log/siyuan:v3.0.17
# IMAGE := ubuntu:20.04
# IMAGE := ubuntu:22.04
# IMAGE := ubuntu:24.04
# IMAGE := ubuntu:24.10
# IMAGE := golang:1.22.5
# IMAGE := python:3.12.5
# IMAGE := golang:1.22.5-alpine3.20
# IMAGE := alpine:3.20
# IMAGE := kindest/node:v1.25.8
# IMAGE := registry:2.8
# IMAGE := kindest/node:v1.25.16
# IMAGE := kindest/node:v1.27.0
# IMAGE := redhat/ubi8:8.4
# IMAGE := nginx:1.27.2
# IMAGE := mysql:5.7
# IMAGE := redis:7.0
# IMAGE := cptactionhank/atlassian-confluence:7.9.3
# IMAGE = klausmeyer/docker-registry-browser:1.7.5
# IMAGE = quay.io/coreos/etcd:v3.4.32
IMAGE = bitnami/etcd:3.5
# IMAGE = sigoden/dufs:v0.42.0
# IMAGE := mysql:8.0
# IMAGE := python:3.11-slim-bullseye
# IMAGE := python:2.7.18

# DOCKER_PROXY := m.daocloud.io/docker.io
DOCKER_PROXY := docker.1ms.run

SRC_IMAGE := $(DOCKER_PROXY)/$(IMAGE)
DST_IMAGE := $(REGISTRY_URL)/$(IMAGE)


pull-origin:		## download origin image and tag
	docker pull $(SRC_IMAGE)
	@echo
	docker tag $(SRC_IMAGE) $(IMAGE)
	@echo
	docker rmi $(SRC_IMAGE)

build:		## download origin image and tag
	docker pull $(SRC_IMAGE)
	@echo
	docker tag $(SRC_IMAGE) $(DST_IMAGE)
	@echo
	docker rmi $(SRC_IMAGE)

push: 		## push image to registry
	docker push $(DST_IMAGE)

pull:		## pull image from registry
	docker pull $(DST_IMAGE)

check:		## check registry
	curl http://$(REGISTRY_URL)/v2/_catalog

all: build push check



# 替换所有/为_, 替换所有:为_
SAVE_IMAGE := ./saves/$(shell echo "$(IMAGE)" | sed 's/\//_/g' | sed 's/:/_/g').img

save: 	# save
	@echo "source image: $(IMAGE)"
	@echo "save to:      $(SAVE_IMAGE)"
	@if [ ! -d "./saves" ]; then set -x; mkdir -p ./saves; fi
	@if [ -f ${SAVE_IMAGE} ]; then set -x; rm ${SAVE_IMAGE}; fi
	docker save -o ${SAVE_IMAGE} ${DST_IMAGE}
	@echo
	ls -alh ./saves

load:		## load
	# docker image rm $(SAVE_IMAGE)
	docker load -i $(SAVE_IMAGE) 

