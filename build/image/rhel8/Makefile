
include $(INC_DIR)/Makefile.common

############################################################
# base 
############################################################

RHEL_IMAGE=base-rhel-8.4:latest
RHEL_NAME=base-rhel8

build-base: 
	docker build -f ./Dockerfile.base --progress=plain -t $(RHEL_IMAGE) $(BUILD_DIR)

start-base: 
	docker run --rm -it \
	--name $(RHEL_NAME) --hostname $(RHEL_NAME) \
	$(RHEL_IMAGE)

stop-base:
	docker stop $(RHEL_NAME)
	docker rm $(RHEL_NAME)

enter-base:
	docker exec -it $(RHEL_NAME) zsh

############################################################
# devc
############################################################

DEVC_IMAGE_CENTOS=devc-rhel-8.4:latest
DEVC_NAME_CENTOS=rhel8

build: 
	docker build -f ./Dockerfile.devc --progress=plain -t $(DEVC_IMAGE_CENTOS) $(BUILD_DIR)

start: 
	docker run $(DEVC_WITH_OPTIONS) \
	--name $(DEVC_NAME_CENTOS) --hostname $(DEVC_NAME_CENTOS) \
	$(DEVC_IMAGE_CENTOS)

stop:
	docker stop $(DEVC_NAME_CENTOS)
	docker rm $(DEVC_NAME_CENTOS)

enter:
	docker exec -it $(DEVC_NAME_CENTOS) zsh

