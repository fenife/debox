
include $(INC_DIR)/Makefile.common
include ./Makefile.venv

CODE_DIR=/wine/code

############################################################
# build
############################################################
VMC_IMAGE=devc-vmc:latest

build: 		## docker build image
	docker build -f ./Dockerfile -t $(VMC_IMAGE) .

############################################################
# net
############################################################
DEVC_NET=devc-net

net-add:		## add devc net
	docker network create --driver=bridge \
	--subnet=172.18.0.0/24 --gateway=172.18.0.1 \
	-o com.docker.network.bridge.name=$(DEVC_NET) $(DEVC_NET)

net-del:
	docker network rm $(DEVC_NET)

############################################################
# vmc1
############################################################
VMC_NAME1=vmc1
VMC_IP1=172.18.0.2

start1: 		## docker start vmc1
	docker run -d $(DEVC_WITH_OPTIONS) \
	--name $(VMC_NAME1) --hostname $(VMC_NAME1) \
	--network $(DEVC_NET) --ip $(VMC_IP1) \
	-v $(CODE_DIR):$(CODE_DIR) \
	-v $(VENV_DIR):$(VENV_DIR) \
	-p 8010:8010 \
	$(VMC_IMAGE)


stop1:		## docker stop vmc1
	docker stop $(VMC_NAME1)
	docker rm $(VMC_NAME1)

at1:		## attach to vmc1
	docker exec -it $(VMC_NAME1) zsh

