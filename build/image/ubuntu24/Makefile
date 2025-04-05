
include $(INC_DIR)/Makefile.inc

############################################################
# base 
############################################################

UBUNTU_BASE_IMAGE=$(IMAGE_ME_NS)/base-ubuntu-24.04:latest
UBUNTU_BASE_NAME=base-ubuntu24

build-base: 
	docker build -f ./Dockerfile.base -t $(UBUNTU_BASE_IMAGE) $(BUILD_DIR)

start-base: 
	docker run --rm -it \
	--name $(UBUNTU_BASE_NAME) --hostname $(UBUNTU_BASE_NAME) \
	$(UBUNTU_BASE_IMAGE)

stop-base:
	docker stop $(UBUNTU_BASE_NAME)
	docker rm $(UBUNTU_BASE_NAME)

enter-base:
	docker exec -it $(UBUNTU_BASE_NAME) bash

############################################################
# local image
############################################################

UBUNTU_IMAGE=$(IMAGE_ME_NS)/local-ubuntu-24.04:latest
UBUNTU_NAME=ubuntu24

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


