include $(INC_DIR)/Makefile.inc

WEBOX_IMAGE=$(REGISTRY_URL)/devel/webox-v2:latest
WEBOX_NAME=webox-v2
WEBOX_CODE_DIR=$(ICODE_DIR)/webox_v2
WEBOX_LOG_DIR=/wine/var/log/webox
WEBOX_VENV_DIR=/wine/venv/icode
WEBOX_PORT=8012

############################################################
# venv and prepare
############################################################

venv:	## create venv dir
	python3 -m venv $(WEBOX_VENV_DIR)

pip:	## install requirements 
	$(WEBOX_VENV_DIR)/bin/pip3 install -r $(ICODE_DIR)/requirements.txt

pre:	## prepare
	mkdir -p $(WEBOX_LOG_DIR)

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
	-p $(WEBOX_PORT):$(WEBOX_PORT) \
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
	run main.py --server.port $(WEBOX_PORT)

