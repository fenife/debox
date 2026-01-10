include $(INC_DIR)/Makefile.inc

SERVER_GO_IMAGE=$(REGISTRY_URL)/devel/server-go:latest
SERVER_GO_NAME=server-go
SERVER_GO_CODE_DIR=$(ICODE_DIR)/server-go

pre:
	go install github.com/swaggo/swag/cmd/swag@v1.16.6

build: 		## docker build image
	docker build -f ./Dockerfile \
	-t $(SERVER_GO_IMAGE) $(SERVER_GO_CODE_DIR)

start: 		## docker start container
	docker run --rm -it \
	--name $(SERVER_GO_NAME) --hostname $(SERVER_GO_NAME) \
	--add-host="dev.local:$(HOST_IP)"  \
	-p 8020:8020 \
	-v $(SHARE_DIR):$(SHARE_DIR) \
	-v $(ICODE_DIR):$(ICODE_DIR) \
	$(SERVER_GO_IMAGE)

stop:		## docker stop container
	docker stop $(SERVER_GO_NAME)
	docker rm $(SERVER_GO_NAME)

at:		## attach to container
	docker exec -it $(SERVER_GO_NAME) zsh


############################################################
# service
############################################################
migrate:		## db migrate
	cd $(SERVER_GO_CODE_DIR); \
	go run ./cmd/migrate

# localhost:8020/swagger/index.html
swag:			## swag
	cd $(SERVER_GO_CODE_DIR); \
	swag init

dev: swag 		## start service
	cd $(SERVER_GO_CODE_DIR); \
	go run .	

############################################################
# db
############################################################

MYSQL_CONN = mysql -hdev.local -P3306 -utest -ptest

db:
	$(MYSQL_CONN)


