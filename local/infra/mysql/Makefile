include $(INC_DIR)/Makefile.inc

MYSQL_IMAGE=$(REGISTRY_URL)/mysql:5.7
MYSQL_NAME=mysql-5.7
MYSQL_DATA_DIR=/wine/var/mysql
MYSQL_ROOT_PASSWORD=root

pre:
	mkdir -p $(MYSQL_DATA_DIR)

pull:		## pull mysql
	docker pull $(MYSQL_IMAGE)

start:		## start mysql
	docker run -d --restart unless-stopped \
	--name $(MYSQL_NAME) \
	-p 3306:3306 \
	-v $(MYSQL_DATA_DIR):/var/lib/mysql \
	-e MYSQL_ROOT_PASSWORD=$(MYSQL_ROOT_PASSWORD) \
	$(MYSQL_IMAGE) 

stop:		## stop mysql
	docker stop $(MYSQL_NAME)
	docker rm $(MYSQL_NAME)

restart:	## restart mysql
	docker restart $(MYSQL_NAME)

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
