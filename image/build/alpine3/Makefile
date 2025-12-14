
include $(INC_DIR)/Makefile.inc

############################################################
# base 
############################################################

ALPINE_BASE_IMAGE=$(REGISTRY_URL)/devel/alpine-3.20-base:latest
ALPINE_BASE_NAME=alpine3-base

build-base: 		## build base
	docker build -f ./Dockerfile.base \
	--build-arg DFS_PRIV_URL=${DFS_PRIV_URL} \
	--build-arg DFS_PUB_URL=${DFS_PUB_URL} \
	-t $(ALPINE_BASE_IMAGE) .

start-base: 		## start base
	docker run --rm -it \
	--name $(ALPINE_BASE_NAME) --hostname $(ALPINE_BASE_NAME) \
	$(ALPINE_BASE_IMAGE)

stop-base:		## stop base
	docker stop $(ALPINE_BASE_NAME)
	docker rm $(ALPINE_BASE_NAME)

enter-base:		## attach base
	docker exec -it $(ALPINE_BASE_NAME) bash

push-base:		## push base
	docker push ${ALPINE_BASE_IMAGE}

############################################################
# devc
############################################################

DEVC_IMAGE_ALPINE=devc-alpine-3.20:latest
DEVC_NAME_ALPINE=alpine3

build: 		## build
	docker build -f ./Dockerfile.devc --progress=plain -t $(DEVC_IMAGE_ALPINE) $(BUILD_DIR)

start: 		## start
	docker run --rm -it \
	--name $(DEVC_NAME_ALPINE) --hostname $(DEVC_NAME_ALPINE) \
	$(DEVC_IMAGE_ALPINE)

stop:		## stop
	docker stop $(DEVC_NAME_ALPINE)
	docker rm $(DEVC_NAME_ALPINE)

enter:		## attach
	docker exec -it $(DEVC_NAME_ALPINE) bash

save:		## save
	$(call _save_image,$(DEVC_IMAGE_ALPINE))

load:		## load
	$(call _load_image,$(DEVC_IMAGE_ALPINE))
	
