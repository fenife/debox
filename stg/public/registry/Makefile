include $(INC_DIR)/Makefile.inc

REGISTRY_NAME = docker-registry
REGISTRY_IMAGE = $(REGISTRY_URL)/registry:2.8
REGISTRY_PORT = 8810
REGISTRY_DATA = /wine/var/registry

REGISTRY_UI_NAME = docker-registry-ui
REGISTRY_UI_IMAGE = $(REGISTRY_URL)/klausmeyer/docker-registry-browser:1.7.5
REGISTRY_UI_PORT = 8820

pre:	## prepare
	mkdir -p $(REGISTRY_DATA)

start:	## start registry
	docker run -d --restart on-failure:3 \
	--name $(REGISTRY_NAME) \
	-p $(REGISTRY_PORT):5000 \
	-v $(REGISTRY_DATA):/var/lib/registry \
	$(REGISTRY_IMAGE)

stop:		## stop registry
	docker stop $(REGISTRY_NAME)

rm:			## rm registry
	docker rm $(REGISTRY_NAME)

restart:
	docker restart $(REGISTRY_NAME)

check:		## check registry
	curl http://$(REGISTRY_URL)/v2/_catalog


ui-start:		## start registry ui
	docker run -d --restart on-failure:3 \
	--name $(REGISTRY_UI_NAME) \
	-p $(REGISTRY_UI_PORT):8080 \
	--link $(REGISTRY_NAME) \
	-e SECRET_KEY_BASE=123 \
	-e DOCKER_REGISTRY_URL=http://$(REGISTRY_NAME):5000/v2 \
	$(REGISTRY_UI_IMAGE)

ui-stop:		## start registry ui
	docker stop $(REGISTRY_UI_NAME)

ui-rm:			## rm registry ui
	docker rm $(REGISTRY_UI_NAME)

ui-restart:
	docker restart $(REGISTRY_UI_NAME)
