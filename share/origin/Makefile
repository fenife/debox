
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
IMAGE := registry:2.8
# IMAGE := kindest/node:v1.25.16
# IMAGE := kindest/node:v1.27.0
# IMAGE := redhat/ubi8:8.4
# IMAGE := nginx:1.27.2
# IMAGE := mysql:5.7
# IMAGE := redis:7.0
# IMAGE := cptactionhank/atlassian-confluence:7.9.3

DOCKER_PROXY := m.daocloud.io/docker.io
# DOCKER_PROXY := docker.rainbond.cc

DOCKER_PROXY_IMAGE := $(DOCKER_PROXY)/$(IMAGE)

pull:
	docker pull $(DOCKER_PROXY_IMAGE)
	docker tag $(DOCKER_PROXY_IMAGE) $(IMAGE)
	docker rmi $(DOCKER_PROXY_IMAGE)
