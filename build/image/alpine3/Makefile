
include $(INC_DIR)/Makefile.common

############################################################
# base 
############################################################

BASE_IMAGE_ALPINE=base-alpine-3.20:latest
BASE_NAME_ALPINE=base-alpine3

build-base: 		## build
	docker build -f ./Dockerfile.base -t $(BASE_IMAGE_ALPINE) $(IMAGE_BUILD_DIR)

start-base: 		## start
	docker run --rm -it \
	--name $(BASE_NAME_ALPINE) --hostname $(BASE_NAME_ALPINE) \
	$(BASE_IMAGE_ALPINE)

stop-base:		## stop
	docker stop $(BASE_NAME_ALPINE)
	docker rm $(BASE_NAME_ALPINE)

enter-base:		## attach
	docker exec -it $(BASE_NAME_ALPINE) bash

############################################################
# devc
############################################################

DEVC_IMAGE_ALPINE=devc-alpine-3.20:latest
DEVC_NAME_ALPINE=alpine3

build: 		## build
	docker build -f ./Dockerfile.devc -t $(DEVC_IMAGE_ALPINE) $(IMAGE_BUILD_DIR)

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
	
