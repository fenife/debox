
include $(INC_DIR)/Makefile.common

############################################################
# base 
############################################################

BASE_IMAGE_CENTOS=base-centos-7.9:latest
BASE_NAME_CENTOS=base-centos7

build-base: 
	docker build -f ./Dockerfile.base -t $(BASE_IMAGE_CENTOS) $(IMAGE_BUILD_DIR)

start-base: 
	docker run --rm -it --privileged \
	--add-host="$(HOST_NAME):$(HOST_IP)"  \
	--name $(BASE_NAME_CENTOS) --hostname $(BASE_NAME_CENTOS) \
	$(BASE_IMAGE_CENTOS)

stop-base:
	docker stop $(BASE_NAME_CENTOS)
	docker rm $(BASE_NAME_CENTOS)

enter-base:
	docker exec -it $(BASE_NAME_CENTOS) zsh

############################################################
# devc
############################################################

DEVC_IMAGE_CENTOS=devc-centos-7.9:latest
DEVC_NAME_CENTOS=centos7

build: 
	docker build -f ./Dockerfile.devc --progress=plain -t $(DEVC_IMAGE_CENTOS) $(IMAGE_BUILD_DIR)

start: 
	docker run $(DEVC_WITH_OPTIONS) \
	--name $(DEVC_NAME_CENTOS) --hostname $(DEVC_NAME_CENTOS) \
	$(DEVC_IMAGE_CENTOS)

stop:
	docker stop $(DEVC_NAME_CENTOS)
	docker rm $(DEVC_NAME_CENTOS)

enter:
	docker exec -it $(DEVC_NAME_CENTOS) zsh

