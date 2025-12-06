
CUR_DIR := $(shell pwd)
PUB_DIR := $(shell readlink -f $(CUR_DIR)/../..)
BASE_DIR := /wine

MYSQL_IMAGE=$(REGISTRY_URL)/library/mysql:5.7
MYSQL_NAME=mysql-5.7
MYSQL_DATA_DIR=${BASE_DIR}/var/lib/mysql5.7

MYSQL_ROOT_PASSWORD=root

help:
	@echo "usage:"
	@echo "  pub dir:  ${PUB_DIR}"
	@echo "  base dir: ${BASE_DIR}"
	@echo "  data dir: ${MYSQL_DATA_DIR}"
	@echo
	@echo "  pre		- 准备 var data 目录"
	@echo "  pull		- pull"
	@echo "  start		- start"
	@echo "  stop		- stop"
	@echo "  restart	- restart"
	@echo "  at			- docker enter (exec)"
	@echo "  root		- connect to mysql by root"
	@echo "  test		- connect to mysql by test"

h: help

pre:
	if [ -f $(MYSQL_DATA_DIR) ]; then set -x; rm $(MYSQL_DATA_DIR); fi
	@echo
	ls -alh $(MYSQL_DATA_DIR)

pull:		## pull mysql
	docker pull $(MYSQL_IMAGE)

start:		## start mysql
	docker run -d --restart always \
	--name $(MYSQL_NAME) \
	-p 3306:3306 \
	-v $(MYSQL_DATA_DIR):/var/lib/mysql \
	-e MYSQL_ROOT_PASSWORD=$(MYSQL_ROOT_PASSWORD) \
	$(MYSQL_IMAGE) 

stop:		## stop mysql
	docker stop $(MYSQL_NAME)
	docker rm $(MYSQL_NAME)

restart: stop start

at:		## enter mysql
	docker exec -it $(MYSQL_NAME) bash

root:	## connect to mysql by root
	mysql -h127.0.0.1 -P3306 -uroot -p$(MYSQL_ROOT_PASSWORD)

test:	## connect to mysql by test
	mysql -h127.0.0.1 -P3306 -utest -ptest

# 创建用户
# CREATE USER 'test' IDENTIFIED BY 'test';
# 用户授权
# GRANT ALL PRIVILEGES ON *.* TO test@'%' IDENTIFIED BY 'test'; 
# 刷新
# flush privileges;
