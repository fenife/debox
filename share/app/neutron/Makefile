
include $(INC_DIR)/Makefile.inc

NEUTRON_CODE_DIR=/wine/code/neutron
VENV_DIR=/wine/venv/neutron

PYTHON=$(VENV_DIR)/bin/python2

WITH_CONFIG_FILE=--config-file $(NEUTRON_CODE_DIR)/etc/neutron.conf \
			     --config-dir $(NEUTRON_CODE_DIR)/etc


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

