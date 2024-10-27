
include $(INC_DIR)/Makefile.common

############################################################
# base 
############################################################

UBUNTU_IMAGE=base-ubuntu-24.04:latest
UBUNTU_NAME=base-ubuntu24

build-base: 
	docker build -f ./Dockerfile.base --progress=plain -t $(UBUNTU_IMAGE) $(BUILD_DIR)

start-base: 
	docker run --rm -it \
	--name $(UBUNTU_NAME) --hostname $(UBUNTU_NAME) \
	$(UBUNTU_IMAGE)

stop-base:
	docker stop $(UBUNTU_NAME)
	docker rm $(UBUNTU_NAME)

enter-base:
	docker exec -it $(UBUNTU_NAME) zsh

############################################################
# devc
############################################################

DEVC_IMAGE_UBUNTU=devc-ubuntu-24.04:latest
DEVC_NAME_UBUNTU=ubuntu24

build: 
	docker build -f ./Dockerfile.devc --progress=plain -t $(DEVC_IMAGE_UBUNTU) $(BUILD_DIR)

# docker run $(DEVC_WITH_OPTIONS) 
start: 
	docker run --rm -it --privileged \
	--name $(DEVC_NAME_UBUNTU) --hostname $(DEVC_NAME_UBUNTU) \
	$(DEVC_IMAGE_UBUNTU)

stop:
	docker stop $(DEVC_NAME_UBUNTU)
	docker rm $(DEVC_NAME_UBUNTU)

enter:
	docker exec -it $(DEVC_NAME_UBUNTU) zsh


