include $(INC_DIR)/Makefile.inc

REGISTRY_NAME = docker-registry
REGISTRY_PORT = 9000
REGISTRY_DATA = /wine/var/registry

REGISTRY_UI_NAME = docker-registry-ui
REGISTRY_UI_IMAGE = $(REGISTRY_URL)/joxit/docker-registry-ui:2.5.7 
REGISTRY_UI_PORT = 9010

start:		## start registry ui
	docker run -d --restart on-failure:3 \
	--add-host="$(REGISTRY_HOST):$(HOST_IP)"  \
	--name $(REGISTRY_UI_NAME) \
	-p $(REGISTRY_UI_PORT):80 \
	-e SINGLE_REGISTRY=true \
	-e REGISTRY_TITLE="Docker Registry UI" \
	-e DELETE_IMAGES=true \
	-e SHOW_CONTENT_DIGEST=true \
	-e NGINX_PROXY_PASS_URL=http://$(REGISTRY_HOST):$(REGISTRY_PORT)/v2 \
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

rm:			## rm registry ui
	docker rm $(REGISTRY_UI_NAME)

restart:
	docker restart $(REGISTRY_UI_NAME)
