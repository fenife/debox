
include /wine/devbox/opt/include/Makefile.common

.PHONY: mysql cfn push pull
.PHONY: up stop exec clean

INSTALL_DIR=/opt/atlassian/confluence/
DATA_DIR=/wine/var/lib/cfn/
CONTAINER_NAME=confluence

pre:
	mkdir -p $(DATA_DIR)/confluence
	mkdir -p $(DATA_DIR)/mysql

ls:
	ls -alh $(DATA_DIR)/confluence
	ls -alh $(DATA_DIR)/mysql

build-mysql:
	docker build -f mysql.Dockerfile -t mysql:5.7.30-confluence .	

build-cfn:
	docker build -f confluence.Dockerfile -t confluence:7.9.3-agented .

tag:
	#docker tag cptactionhank/atlassian-confluence:7.9.3 fenife/atlassian-confluence:7.9.3
	docker tag mysql:5.7.30-confluence fenife/mysql:5.7.30-confluence
	docker tag confluence:7.9.3-agented fenife/confluence:7.9.3-agented

push:
	docker push fenife/mysql:5.7.30-confluence
	docker push fenife/confluence:7.9.3-agented

pull:
	docker pull fenife/mysql:5.7.30-confluence
	docker pull fenife/confluence:7.9.3-agented

start:
	docker compose up 

startd:
	docker compose up -d

stop:
	docker compose stop
	docker rm $(CONTAINER_NAME)
	docker rm mysql-confluence

exec:
	docker exec -it confluence /bin/bash 

clean:
	sudo rm -rf $(DATA_DIR)/*

at: exec



DB_CONN=mysql -h127.0.0.1 -P3308 -uroot -proot

conn:
	$(DB_CONN)

db-create:
	$(DB_CONN) -e "create database confluence;"
	$(DB_CONN) -e "show databases;"

jdbc:
	@echo "jdbc:mysql://mysql-confluence:3306/confluence?characterEncoding=utf8&useUnicode=true&useSSL=false"	


# EMAIL=xxx@xxx.com
EMAIL=fenife@163.com
NOTE_NAME=note
ADDR=http://$(HOST_IP)
# 设置 - 一般配置 - 授权细节(可在页面搜索) - 服务器ID
SERVER_ID=BA8O-5P5P-QN2T-3YI8
 
auth-server:
	docker exec $(CONTAINER_NAME) \
	java -jar $(INSTALL_DIR)/atlassian-agent.jar \
	-d -m ${EMAIL} -n ${NOTE_NAME} \
	-p conf -o ${ADDR} \
	-s ${SERVER_ID}

APPKEY=conf
# APPKEY=cz.morosystems.atlassian.plugin.easymind
# APPKEY = com.mxgraph.confluence.plugins.diagramly
APPKEY=com.stiltsoft.confluence.plugin.tablefilter.tablefilter

auth-app:
	docker exec $(CONTAINER_NAME) \
	java -jar $(INSTALL_DIR)/atlassian-agent.jar \
	-d -m ${EMAIL} -n ${NOTE_NAME} \
	-p $(APPKEY) -o ${ADDR} \
	-s ${SERVER_ID} 


# jdbc:mysql://192.168.0.121:3308/confluence?characterEncoding=utf8&useUnicode=true&useSSL=false
# jdbc:mysql://192.168.0.121:3308/confluence?characterEncoding=utf8&useUnicode=true&useSSL=false&serverTimezone=UTC
