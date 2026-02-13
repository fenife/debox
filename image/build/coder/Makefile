
include $(INC_DIR)/Makefile.inc

############################################################
# base 
############################################################

CODER_IMAGE=$(REGISTRY_URL)/devel/coder-ubuntu-22.04:latest
CODER_NAME=coder

build: 	## build
	docker build -f ./Dockerfile \
	-t $(CODER_IMAGE) ${DFS_DIR}

start: 	## start
	docker run --rm -it \
	--name $(CODER_NAME) --hostname $(CODER_NAME) \
	$(CODER_IMAGE)

stop:		## stop 
	docker stop $(CODER_NAME)
	docker rm $(CODER_NAME)

at:		## enter / attach
	docker exec -it $(CODER_NAME) bash

push:		## push
	docker push $(CODER_IMAGE)
