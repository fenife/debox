## see: https://github.com/Joxit/docker-registry-ui

REGISTRY_NAME = docker-registry
REGISTRY_PORT = 9000

REGISTRY_UI_NAME = docker-registry-ui
REGISTRY_UI_IMAGE = $(REGISTRY_URL)/joxit/docker-registry-ui:2.5.7 
REGISTRY_UI_PORT = 9010

help:
	@echo "usage:"
	@echo
	@echo "  start		- start registry ui"
	@echo "  stop		- stop registry ui"
	@echo "  restart	- restart registry ui"

h: help

# 	--add-host="$(REGISTRY_HOST):$(HOST_IP)"  

start:		## start registry ui
	docker run -d --restart unless-stopped \
	--name $(REGISTRY_UI_NAME) \
	-p $(REGISTRY_UI_PORT):80 \
	--link ${REGISTRY_NAME} \
	-e SINGLE_REGISTRY=true \
	-e REGISTRY_TITLE="Docker Registry UI" \
	-e DELETE_IMAGES=true \
	-e SHOW_CONTENT_DIGEST=true \
	-e NGINX_PROXY_PASS_URL=http://$(REGISTRY_NAME):5000/v2 \
	-e SHOW_CATALOG_NB_TAGS=true \
	-e CATALOG_MIN_BRANCHES=1 \
	-e CATALOG_MAX_BRANCHES=1 \
	-e TAGLIST_PAGE_SIZE=100 \
	-e REGISTRY_SECURED=false \
	-e CATALOG_ELEMENTS_LIMIT=1000 \
	$(REGISTRY_UI_IMAGE)

stop:		## start registry ui
	docker stop $(REGISTRY_UI_NAME)
	docker rm $(REGISTRY_UI_NAME)

restart:
	docker restart $(REGISTRY_UI_NAME)
