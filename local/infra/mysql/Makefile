
include $(INC_DIR)/Makefile.common

MYSQL_IMAGE=mysql:5.7
MYSQL_NAME=mysql
MYSQL_DATA_DIR=$(ROOT_DIR)/var/mysql
MYSQL_ROOT_PASSWORD=root

.PHONY: start stop

pull:
	docker pull $(MYSQL_IMAGE)

start:
	docker run -d -p 3306:3306 --name $(MYSQL_NAME) \
	-v $(MYSQL_DATA_DIR):/var/lib/mysql \
	-e MYSQL_ROOT_PASSWORD=$(MYSQL_ROOT_PASSWORD) \
	$(MYSQL_IMAGE) 

stop:
	docker stop $(MYSQL_NAME)
	docker rm $(MYSQL_NAME)

restart:
	docker restart $(MYSQL_NAME)

enter:
	docker exec -it $(MYSQL_NAME) bash

root:
	mysql -h127.0.0.1 -P3306 -uroot -p$(MYSQL_ROOT_PASSWORD)

test:
	mysql -h127.0.0.1 -P3306 -utest -ptest

# 创建用户
# CREATE USER 'test' IDENTIFIED BY 'test';
# 用户授权
# GRANT ALL PRIVILEGES ON *.* TO test@'%' IDENTIFIED BY 'test'; 
# 刷新
# flush privileges;
