
include $(INC_DIR)/Makefile.inc

############################################################
# base 
############################################################

UBUNTU_BASE_IMAGE=$(REGISTRY_URL)/devel/ubuntu-22.04-base:latest
UBUNTU_BASE_NAME=ubuntu22-base

build-base: 	## build base
	docker build -f ./Dockerfile.base \
	--build-arg DFS_PRIV_URL=${DFS_PRIV_URL} \
	--build-arg DFS_PUB_URL=${DFS_PUB_URL} \
	-t $(UBUNTU_BASE_IMAGE) .

start-base: 	## start base
	docker run --rm -it \
	--name $(UBUNTU_BASE_NAME) --hostname $(UBUNTU_BASE_NAME) \
	$(UBUNTU_BASE_IMAGE)

stop-base:		## stop base
	docker stop $(UBUNTU_BASE_NAME)
	docker rm $(UBUNTU_BASE_NAME)

enter-base:		## enter base
	docker exec -it $(UBUNTU_BASE_NAME) bash

push-base:		## push base
	docker push $(UBUNTU_BASE_IMAGE)

############################################################
# local image
############################################################

UBUNTU_IMAGE=$(REGISTRY_URL)/devel/ubuntu-22.04-local:latest
UBUNTU_NAME=ubuntu22

build: 
	docker build -f ./Dockerfile.local -t $(UBUNTU_IMAGE) $(BUILD_DIR)

# docker run $(LOCAL_WITH_OPTIONS) 
start: 
	docker run --rm -it --privileged \
	--name $(UBUNTU_NAME) --hostname $(UBUNTU_NAME) \
	-v $(SHARE_DIR):$(SHARE_DIR) \
	$(UBUNTU_IMAGE)

stop:
	docker stop $(UBUNTU_NAME)
	docker rm $(UBUNTU_NAME)

at:
	docker exec -it $(UBUNTU_NAME) zsh


