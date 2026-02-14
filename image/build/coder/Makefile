
include $(INC_DIR)/Makefile.inc

############################################################
# base 
############################################################

CODER_IMAGE=$(REGISTRY_URL)/devel/coder-ubuntu-22.04:latest
CODER_NAME=coder

HOST_UID_GID := $(shell id -u):$(shell id -g)
PWD_CONF = $(shell pwd)/.config

pre:
	mkdir -p $(PWD_CONF)

build: 	## build
	DOCKER_BUILDKIT=1 docker build -f ./Dockerfile \
	-t $(CODER_IMAGE) ${DFS_DIR}

start: 	## start
	docker run --rm -it \
	--name $(CODER_NAME) --hostname $(CODER_NAME) \
	-p 8080:8080 \
	-p 8081:8081 \
	-v $(shell pwd)/etc/config.yaml:/root/.config/code-server/config.yaml  \
	-v $(shell pwd)/etc/settings.json:/root/.local/share/code-server/User/settings.json \
	-v /wine/debox:/wine/debox \
	$(CODER_IMAGE)

# start: 	## start
# 	docker run --rm -it \
# 	--name $(CODER_NAME) --hostname $(CODER_NAME) \
# 	-v "$(HOME)/.config:/home/coder/.config" \
# 	-u "${HOST_UID_GID}" \
# 	-e "DOCKER_USER=${USER}" \
# 	-p 8080:8080 \
# 	-v /wine/debox:/wine/debox \
# 	$(CODER_IMAGE)

# 	-v ~/.config/code-server/config.yaml 
# 	-v ~/.local/share/code-server/

stop:		## stop 
	docker stop $(CODER_NAME)
	docker rm $(CODER_NAME)

at:		## enter / attach
	docker exec -it $(CODER_NAME) bash

push:		## push
	docker push $(CODER_IMAGE)

cm:		## commit
	docker commit ${CODER_NAME} ${CODER_IMAGE}
