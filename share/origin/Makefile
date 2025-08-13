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
# IMAGE = bitnami/etcd:3.5
# IMAGE = sigoden/dufs:v0.42.0
# IMAGE := mysql:8.0
# IMAGE := python:3.11-slim-bullseye
IMAGE := python:2.7.18

# DOCKER_PROXY := m.daocloud.io/docker.io
DOCKER_PROXY := docker.1ms.run

DOCKER_PROXY_IMAGE := $(DOCKER_PROXY)/$(IMAGE)
REGISTRY_IMAGE := $(REGISTRY_URL)/$(IMAGE)

pull-origin:		## download origin image and tag
	docker pull $(DOCKER_PROXY_IMAGE)
	@echo
	docker tag $(DOCKER_PROXY_IMAGE) $(IMAGE)
	@echo
	docker rmi $(DOCKER_PROXY_IMAGE)

build:		## download origin image and tag
	docker pull $(DOCKER_PROXY_IMAGE)
	@echo
	docker tag $(DOCKER_PROXY_IMAGE) $(REGISTRY_IMAGE)
	@echo
	docker rmi $(DOCKER_PROXY_IMAGE)

push: 		## push image to registry
	docker push $(REGISTRY_IMAGE)

pull:		## pull image from registry
	docker pull $(REGISTRY_IMAGE)

check:		## check registry
	curl http://$(REGISTRY_URL)/v2/_catalog

all: build push check
