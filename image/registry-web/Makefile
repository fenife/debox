include $(INC_DIR)/Makefile.inc

REGISTRY_NAME = docker-registry
REGISTRY_IMAGE = $(REGISTRY_URL)/registry:2.8
REGISTRY_PORT = 9000
REGISTRY_DATA = /wine/var/registry

REGISTRY_UI_NAME = docker-registry-web
REGISTRY_UI_IMAGE = $(REGISTRY_URL)/konradkleine/docker-registry-frontend:v2
REGISTRY_UI_PORT = 9020

start:		## start registry ui
	docker run --restart on-failure:3 \
	--add-host="$(REGISTRY_HOST):$(HOST_IP)"  \
	--name $(REGISTRY_UI_NAME) \
	-p $(REGISTRY_UI_PORT):80 \
	-e ENV_DOCKER_REGISTRY_HOST=$(REGISTRY_HOST) \
	-e ENV_DOCKER_REGISTRY_PORT=$(REGISTRY_PORT) \
	$(REGISTRY_UI_IMAGE)

# 	docker run -d --restart on-failure:3 \
# 	--name $(REGISTRY_UI_NAME) \
# 	-p $(REGISTRY_UI_PORT):8080 \
# 	--link $(REGISTRY_NAME) \
# 	-e SECRET_KEY_BASE=123 \
# 	-e DOCKER_REGISTRY_URL=http://$(REGISTRY_NAME):5000/v2 \
# 	$(REGISTRY_UI_IMAGE)

stop:		## start registry ui
	docker stop $(REGISTRY_UI_NAME)

rm:			## rm registry ui
	docker rm $(REGISTRY_UI_NAME)

restart:
	docker restart $(REGISTRY_UI_NAME)
