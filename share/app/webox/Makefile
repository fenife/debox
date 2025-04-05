include $(INC_DIR)/Makefile.inc

CODE_DIR=$(ICODE_DIR)/webox
LOG_DIR=/wine/var/log/webox
VENV_DIR=/wine/venv/icode

venv:	## create venv dir
	python3.12 -m venv $(VENV_DIR)

pip:	## install requirements 
	$(VENV_DIR)/bin/pip3 install -r $(CODE_DIR)/requirements.txt

pre:	## prepare
	mkdir -p $(LOG_DIR)

start: 		## start service
	cd $(CODE_DIR); \
	$(VENV_DIR)/bin/python3.12 -m streamlit \
	run main.py --server.port 8010

