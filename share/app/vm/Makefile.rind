
include ../Makefile

############################################################
# network 
############################################################

NET=vm-net
NET0=$(NET)0
NET1=$(NET)1
NET2=$(NET)2

net-add:
	docker network create --driver=bridge --subnet=10.10.0.0/24 --gateway=10.10.0.1 \
	-o com.docker.network.bridge.name=br-$(NET0) $(NET0)
	docker network create --driver=bridge --subnet=10.10.1.0/24 --gateway=10.10.1.1 \
	-o com.docker.network.bridge.name=br-$(NET1) $(NET1)
	docker network create --driver=bridge --subnet=10.10.2.0/24 --gateway=10.10.2.1 \
	-o com.docker.network.bridge.name=br-$(NET2) $(NET2)

net-del:
	docker network rm $(NET0)
	docker network rm $(NET1)
	docker network rm $(NET2)

############################################################
# container
############################################################

VM_IMAGE=dind-alpine-3.19:latest

ZONE=0
VM=1
VM_NAME=vm$(ZONE)$(VM)
VM_NET=$(NET)$(ZONE)
VM_IP=10.10.$(ZONE).1$(VM)

start: 
	docker run --rm -it --privileged --name $(VM_NAME) --hostname $(VM_NAME) \
	--network $(VM_NET) --ip $(VM_IP) \
	$(VM_IMAGE)

stop:
	docker stop $(VM_NAME)
	docker rm $(VM_NAME)

enter:
	docker exec -it $(VM_NAME) bash


############################################################
# load image
############################################################
ALPINE_IMAGE_TAR=dind-alpine-3.19.tar

load:
	docker load -i ${ALPINE_IMAGE_TAR}
