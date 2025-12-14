include $(INC_DIR)/Makefile.inc

# DOCKER_PROXY = m.daocloud.io/docker.io
DOCKER_PROXY := docker.1ms.run

# https://docker.aityp.com/s/docker.io
# DOCKER_PROXY := swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io

############################################################
# library
############################################################

# IMAGE_SRC = $(DOCKER_PROXY)/registry:2.8
# IMAGE_REG = $(REGISTRY_URL)/library/registry:2.8
# IMAGE = library/registry:2.8

# IMAGE_SRC = $(DOCKER_PROXY)/joxit/docker-registry-ui:2.5.7
# IMAGE_REG = $(REGISTRY_URL)/joxit/docker-registry-ui:2.5.7
# IMAGE = joxit/docker-registry-ui:2.5.7

# IMAGE_SRC = $(DOCKER_PROXY)/sigoden/dufs:v0.42.0
# IMAGE_REG = $(REGISTRY_URL)/sigoden/dufs:v0.42.0
# IMAGE = sigoden/dufs:v0.42.0

# IMAGE_SRC = $(DOCKER_PROXY)/ubuntu:20.04
# IMAGE_REG = $(REGISTRY_URL)/library/ubuntu:20.04
# IMAGE = library/ubuntu:20.04

# IMAGE_SRC = $(DOCKER_PROXY)/ubuntu:22.04
# IMAGE_REG = $(REGISTRY_URL)/library/ubuntu:22.04
# IMAGE = library/ubuntu:22.04

# IMAGE_SRC = $(DOCKER_PROXY)/ubuntu:24.04
# IMAGE_REG = $(REGISTRY_URL)/library/ubuntu:24.04
# IMAGE = library/ubuntu:24.04

# IMAGE_SRC = $(DOCKER_PROXY)/ubuntu:24.10
# IMAGE_REG = $(REGISTRY_URL)/library/ubuntu:24.10
# IMAGE = library/ubuntu:24.10

# IMAGE_SRC = $(DOCKER_PROXY)/mysql:5.7
# IMAGE_REG = $(REGISTRY_URL)/library/mysql:5.7
# IMAGE = library/mysql:5.7

# IMAGE_SRC = $(DOCKER_PROXY)/kindest/node:v1.24.12
# IMAGE_REG = $(REGISTRY_URL)/kindest/node:v1.24.12
# IMAGE = kindest/node:v1.24.12

# IMAGE_SRC = $(DOCKER_PROXY)/redhat/ubi8:8.4
# IMAGE_REG = $(REGISTRY_URL)/redhat/ubi8:8.4
# IMAGE = redhat/ubi8:8.4

# IMAGE_SRC = $(DOCKER_PROXY)/golang:1.22.5
# IMAGE_REG = $(REGISTRY_URL)/library/golang:1.22.5
# IMAGE = library/golang:1.22.5

# IMAGE_SRC = $(DOCKER_PROXY)/golang:1.25.0
# IMAGE_REG = $(REGISTRY_URL)/library/golang:1.25.0
# IMAGE = library/golang:1.25.0

# IMAGE_SRC = $(DOCKER_PROXY)/golang:1.24-alpine3.20
# IMAGE_REG = $(REGISTRY_URL)/library/golang:1.24-alpine3.20
# IMAGE = library/golang:1.24-alpine3.20

# IMAGE_SRC = $(DOCKER_PROXY)/golang:1.25-alpine3.22
# IMAGE_REG = $(REGISTRY_URL)/library/golang:1.25-alpine3.22
# IMAGE = library/golang:1.25-alpine3.22

# IMAGE_SRC = $(DOCKER_PROXY)/redis:7.0
# IMAGE_REG = $(REGISTRY_URL)/library/redis:7.0
# IMAGE = library/redis:7.0

# IMAGE_SRC = $(DOCKER_PROXY)/python:3.12.5
# IMAGE_REG = $(REGISTRY_URL)/library/python:3.12.5
# IMAGE = library/python:3.12.5

# IMAGE_SRC = $(DOCKER_PROXY)/alpine:3.20
# IMAGE_REG = $(REGISTRY_URL)/library/alpine:3.20
# IMAGE = library/alpine:3.20

IMAGE_SRC = $(DOCKER_PROXY)/alpine:3.22
IMAGE_REG = $(REGISTRY_URL)/library/alpine:3.22
IMAGE = library/alpine:3.22

# IMAGE_SRC = $(DOCKER_PROXY)/nginx:1.27.2
# IMAGE_REG = $(REGISTRY_URL)/library/nginx:1.27.2
# IMAGE = library/nginx:1.27.2

# IMAGE_SRC = $(DOCKER_PROXY)/mysql:8.0
# IMAGE_REG = $(REGISTRY_URL)/library/mysql:8.0
# IMAGE = library/mysql:8.0

# IMAGE_SRC = $(DOCKER_PROXY)/python:2.7.18
# IMAGE_REG = $(REGISTRY_URL)/library/python:2.7.18
# IMAGE = library/python:2.7.18

# IMAGE_SRC = $(DOCKER_PROXY)/busybox:1.36
# IMAGE_REG = $(REGISTRY_URL)/library/busybox:1.36
# IMAGE = library/busybox:1.36

# IMAGE_SRC = $(DOCKER_PROXY)/busybox:1.36-glibc
# IMAGE_REG = $(REGISTRY_URL)/library/busybox:1.36-glibc
# IMAGE = library/busybox:1.36-glibc

# IMAGE_SRC = $(DOCKER_PROXY)/bitnami/etcd:3.5
# IMAGE_REG = $(REGISTRY_URL)/bitnami/etcd:3.5
# IMAGE = bitnami/etcd:3.5

# IMAGE_SRC = $(DOCKER_PROXY)/kindest/node:v1.25.16
# IMAGE_REG = $(REGISTRY_URL)/kindest/node:v1.25.16
# IMAGE = kindest/node:v1.25.16

# IMAGE_SRC = $(DOCKER_PROXY)/kindest/node:v1.27.0
# IMAGE_REG = $(REGISTRY_URL)/kindest/node:v1.27.0
# IMAGE = kindest/node:v1.27.0

# IMAGE = quay.io/coreos/etcd:v3.4.32 ?

############################################################
# other
############################################################

# IMAGE_SRC = $(DOCKER_PROXY)/cptactionhank/atlassian-confluence:7.9.3
# IMAGE_REG = $(REGISTRY_URL)/cptactionhank/atlassian-confluence:7.9.3
# IMAGE = cptactionhank/atlassian-confluence:7.9.3

# IMAGE_SRC = $(DOCKER_PROXY)/b3log/siyuan:v3.4.2
# IMAGE_REG = $(REGISTRY_URL)/b3log/siyuan:v3.4.2
# IMAGE = b3log/siyuan:v3.4.2

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
	docker tag $(IMAGE_SRC) $(IMAGE_REG)
	@echo
	docker rmi $(IMAGE_SRC)

po: pull-origin

push: 		## push image to registry
	docker push $(IMAGE_REG)

pull:		## pull image from registry
	docker pull $(IMAGE_REG)

check:		## check registry
	curl http://$(REGISTRY_URL)/v2/_catalog


# ###########################################################################
# 定义和函数
# ###########################################################################

# DFS_DIR: bashrc 文件中定义
# DFS_URL: bashrc 文件中定义

DFS_IMAGE_DIR = $(DFS_DIR)/images
SAVE_DIR = ./saves

# 镜像文件名，换所有/为_, 替换所有:为_
IMG_RAW = $(shell echo "$(IMAGE)" | sed 's/\//_/g' | sed 's/:/_/g').img
IMG_TAR = $(IMG_RAW).tar.gz

# 镜像保存路径
IMAGE_RAW_FILE = $(SAVE_DIR)/$(IMG_RAW)
IMAGE_TAR_FILE = $(SAVE_DIR)/$(IMG_TAR)
IMAGE_UPLOAD_FILE = $(DFS_IMAGE_DIR)/$(IMG_TAR)

# 函数：删除旧文件（若存在）
# 参数：$1 = 文件路径
define _delete_file
	@echo "清理旧文件: $1"
	@if [ -f "$1" ]; then \
		set -x; rm -f "$1"; \
		echo "旧文件已删除\n"; \
	else \
		echo "无旧文件，跳过清理\n"; \
	fi
endef

# 函数：打印文件详细信息（ls + du）
# 参数：$1 = 文件/目录路径
define _print_file_info
	@echo "\n------------------------------" 
	@echo "文件详情: $1"
	ls -alh $1
	@echo
	du -sh $1
	@echo
	ls $1 | wc -l
endef

############################################################
# save
############################################################

desc:
	@echo "======================================================"
	@echo "Docker 镜像保存/加载脚本配置"
	@echo "======================================================"
	@echo "源镜像:       $(IMAGE_SRC)"
	@echo "目标镜像:     $(IMAGE_REG)"
	@echo "镜像名:       $(IMAGE)"
	@echo "本地保存目录: $(SAVE_DIR)"
	@echo "原始镜像文件: ${IMAGE_RAW_FILE}"
	@echo "压缩包文件:   ${IMAGE_TAR_FILE}"
	@echo "DFS存储路径:  $(DFS_IMAGE_DIR)"
	@echo "======================================================"

info: desc

save: 	# save
	@echo "======================================================"
	@echo "保存镜像: $(IMAGE_REG) -> $(IMAGE_RAW_FILE)"
	@echo "======================================================"
	$(call _delete_file,${IMAGE_RAW_FILE})
	docker save -o ${IMAGE_RAW_FILE} ${IMAGE_REG}
	$(call _print_file_info,${IMAGE_RAW_FILE})

tar:
	@echo "======================================================"
	@echo "压缩镜像: $(IMAGE_RAW_FILE) -> $(IMAGE_TAR_FILE)"
	@echo "======================================================"
	$(call _delete_file,$(IMAGE_TAR_FILE))
	cd ${SAVE_DIR}; tar -czvf ${IMG_TAR} ${IMG_RAW}
	rm -f ${IMAGE_RAW_FILE}
	$(call _print_file_info,${IMAGE_TAR_FILE})

upload:
	@echo "======================================================"
	@echo "上传镜像: $(IMAGE_TAR_FILE) -> $(DFS_IMAGE_DIR)"
	@echo "======================================================"
	$(call _delete_file,$(IMAGE_UPLOAD_FILE))
	cp $(IMAGE_TAR_FILE) $(IMAGE_UPLOAD_FILE)
	@echo
	$(call _print_file_info,${IMAGE_UPLOAD_FILE})

save-image: save tar upload

all: po push save-image

############################################################
# load
############################################################

download:
	@echo "======================================================"
	@echo "下载镜像: ${DFS_URL}/images/${IMG_TAR}"
	@echo "======================================================"
	$(call _delete_file,${IMAGE_TAR_FILE})
	curl -o ${IMAGE_TAR_FILE} ${DFS_URL}/images/${IMG_TAR}
	@echo
	$(call _print_file_info,${IMAGE_TAR_FILE})

untar:
	@echo "======================================================"
	@echo "解压镜像: ${IMAGE_TAR_FILE} -> ${IMAGE_RAW_FILE}"
	@echo "======================================================"
	$(call _delete_file,${IMAGE_RAW_FILE})
	cd ${SAVE_DIR}; tar -xzvf ${IMG_TAR}
	$(call _delete_file,${IMAGE_TAR_FILE})
	$(call _print_file_info,${IMAGE_RAW_FILE})

load:		## load
	@echo "======================================================"
	@echo "加载镜像: ${IMAGE_RAW_FILE} -> Docker (${IMAGE_REG})"
	@echo "======================================================"
	docker image rm ${IMAGE_REG} || true
	docker load -i ${IMAGE_RAW_FILE} 

clean:
	@echo "======================================================"
	@echo "清理本地临时文件"
	@echo "======================================================"
	$(call _delete_file,${IMAGE_RAW_FILE})
	$(call _delete_file,${IMAGE_TAR_FILE})
	$(call _print_file_info,${SAVE_DIR})

ls:
	ls -alh ${SAVE_DIR}
	@echo
	du -sh ${SAVE_DIR}
	@echo
	ls ${SAVE_DIR} | wc -l

