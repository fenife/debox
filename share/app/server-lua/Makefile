include $(INC_DIR)/Makefile.inc

SERVER_LUA_IMAGE=$(REGISTRY_URL)/devel/server-lua:latest
SERVER_LUA_NAME=server-lua
SERVER_LUA_CODE_DIR=$(ICODE_DIR)/server-lua

pre:
	echo

build: 		## docker build image
	docker build -f ./Dockerfile \
	-t $(SERVER_LUA_IMAGE) $(SERVER_LUA_CODE_DIR)

start: 		## docker start container
	docker run --rm -it \
	--name $(SERVER_LUA_NAME) --hostname $(SERVER_LUA_NAME) \
	--add-host="dev.local:$(HOST_IP)"  \
	-p 8030:80 \
	-v $(SHARE_DIR):$(SHARE_DIR) \
	-v $(SERVER_LUA_CODE_DIR):/data/server-lua \
	$(SERVER_LUA_IMAGE)

stop:		## docker stop container
	docker stop $(SERVER_LUA_NAME)
	docker rm $(SERVER_LUA_NAME)

at:		## attach to container
	docker exec -it $(SERVER_LUA_NAME) bash

