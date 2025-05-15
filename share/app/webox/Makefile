include $(INC_DIR)/Makefile.inc

WEBOX_IMAGE=$(IMAGE_ME_NS)/webox:latest
WEBOX_NAME=webox
WEBOX_CODE_DIR=$(ICODE_DIR)/webox
WEBOX_LOG_DIR=/webox/var/log/webox
WEBOX_VENV_DIR=/wine/venv/icode


############################################################
# venv and prepare
############################################################

venv:	## create venv dir
	python3 -m venv $(WEBOX_VENV_DIR)

pip:	## install requirements 
	$(WEBOX_VENV_DIR)/bin/pip3 install -r $(ICODE_DIR)/requirements.txt

pre:	## prepare
	mkdir -p $(LOG_DIR)

############################################################
# build
############################################################

build: 		## docker build image
	docker build -f ./Dockerfile \
	-t $(WEBOX_IMAGE) $(WEBOX_CODE_DIR)

start: 		## docker start container
	docker run --rm -it \
	--name $(WEBOX_NAME) --hostname $(WEBOX_NAME) \
	--add-host="dev.local:$(HOST_IP)"  \
	-p 8010:8010 \
	-v $(SHARE_DIR):$(SHARE_DIR) \
	-v $(ICODE_DIR):$(ICODE_DIR) \
	-v $(VENV_DIR):$(VENV_DIR) \
	$(WEBOX_IMAGE)

stop:		## docker stop container
	docker stop $(WEBOX_NAME)
	docker rm $(WEBOX_NAME)

at:		## attach to container
	docker exec -it $(WEBOX_NAME) zsh

############################################################
# service
############################################################

dev: 		## start service
	cd $(WEBOX_CODE_DIR); \
	$(WEBOX_VENV_DIR)/bin/python3 -m streamlit \
	run main.py --server.port 8010

