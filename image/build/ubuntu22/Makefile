
include $(INC_DIR)/Makefile.inc

UBUNTU_IMAGE=$(REGISTRY_URL)/devel/ubuntu-22.04:latest
UBUNTU_NAME=ubuntu22

build: 		## build
	docker build -f ./Dockerfile -t $(UBUNTU_IMAGE) $(DFS_DIR)

start: 	## start
	docker run --rm -it --privileged \
	--name $(UBUNTU_NAME) --hostname $(UBUNTU_NAME) \
	-v $(SHARE_DIR):$(SHARE_DIR) \
	$(UBUNTU_IMAGE)

stop:	## stop
	docker stop $(UBUNTU_NAME)
	docker rm $(UBUNTU_NAME)

at:		## attach
	docker exec -it $(UBUNTU_NAME) zsh

push:	## push
	docker push $(UBUNTU_IMAGE)

