include $(INC_DIR)/Makefile.inc

REGISTRY_NAME = docker-registry
REGISTRY_IMAGE = registry:2.8
REGISTRY_PORT = 8810
REGISTRY_DATA = /wine/var/registry

REGISTRY_UI_NAME = docker-registry
REGISTRY_UI_IMAGE = registry:2
REGISTRY_UI_PORT = 8820

pre:	## prepare
	mkdir -p $(REGISTRY_DATA)

start:	## start registry
	docker run -d --name $(REGISTRY_NAME) \
	-p $(REGISTRY_PORT):5000 \
	-v $(REGISTRY_DATA):/var/lib/registry \
	$(REGISTRY_IMAGE)

stop:		## stop registry
	docker stop $(REGISTRY_NAME)

rm:			## rm registry
	docker rm $(REGISTRY_NAME)

check:		## check registry
	curl http://$(REGISTRY_HOST)/v2/_catalog



