
include $(INC_DIR)/Makefile.inc

NEUTRON_CODE_DIR=/wine/code/neutron-24.0.1
VENV_DIR=/wine/venv/neutron24

PYTHON=$(VENV_DIR)/bin/python3

WITH_CONFIG_FILE=--config-file $(NEUTRON_CODE_DIR)/etc/neutron.conf \
			     --config-dir $(NEUTRON_CODE_DIR)/etc


NEUTRON_IMAGE=neutron-24.0.1:latest
NEUTRON_NAME=neutron

build: 		## docker build image 
	docker build -f ./Dockerfile -t $(NEUTRON_IMAGE) .

start: 		## docker start container
	docker run $(DEVC_WITH_OPTIONS) \
	--name $(NEUTRON_NAME) --hostname $(NEUTRON_NAME) \
	-p 9696:9696 \
	-v $(NEUTRON_CODE_DIR):$(NEUTRON_CODE_DIR) \
	--privileged=true \
	$(NEUTRON_IMAGE)

stop:		## docker stop container
	docker stop $(NEUTRON_NAME)
	docker rm $(NEUTRON_NAME)

enter:		## attach to container
	docker exec -it $(NEUTRON_NAME) zsh



venv:
	virtualenv $(VENV_DIR)

pip:
	$(VENV_DIR)/bin/pip2 install --no-deps \
		pbr==1.8 Paste==2.0.2 PasteDeploy==1.5.0 aioeventlet==0.5.2
	$(VENV_DIR)/bin/pip2 install --no-deps -r ./requirements.txt

cd:		## cd code dir
	cd $(NEUTRON_CODE_DIR)	

setup:	## python setup
	cd $(NEUTRON_CODE_DIR); \
	python2 ./setup.py develop

start: setup		## start neutron service
	python2 /usr/bin/neutron-server $(WITH_CONFIG_FILE)

db-migrate: 		## db migrate data
	python2 /usr/bin/neutron-db-manage $(WITH_CONFIG_FILE) current

db-upgrade:			## db migrate data to heads
	python2 /usr/bin/neutron-db-manage $(WITH_CONFIG_FILE) upgrade heads

