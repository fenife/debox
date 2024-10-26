
include $(INC_DIR)/Makefile.common

############################################################
# base 
############################################################

BASE_IMAGE_UBUNTU=base-ubuntu-24.04:latest
BASE_NAME_UBUNTU=base-ubuntu24

build-base: 
	docker build -f ./Dockerfile.base -t $(BASE_IMAGE_UBUNTU) $(IMAGE_BUILD_DIR)

start-base: 
	docker run --rm -it --privileged \
	--add-host="$(HOST_NAME):$(HOST_IP)"  \
	--name $(BASE_NAME_UBUNTU) --hostname $(BASE_NAME_UBUNTU) \
	$(BASE_IMAGE_UBUNTU)

stop-base:
	docker stop $(BASE_NAME_UBUNTU)
	docker rm $(BASE_NAME_UBUNTU)

enter-base:
	docker exec -it $(BASE_NAME_UBUNTU) zsh

############################################################
# testc
############################################################

DEVC_IMAGE_UBUNTU=devc-ubuntu-24.04:latest
DEVC_NAME_UBUNTU=ubuntu24

build: 
	docker build -f ./Dockerfile.devc -t $(DEVC_IMAGE_UBUNTU) $(IMAGE_BUILD_DIR)

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


