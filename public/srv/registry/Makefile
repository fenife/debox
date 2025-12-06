include $(INC_DIR)/Makefile.inc

REGISTRY_NAME = docker-registry
REGISTRY_IMAGE = $(REGISTRY_URL)/library/registry:2.8
REGISTRY_PORT = 9000
REGISTRY_DATA = /wine/var/registry

pre:	## prepare
	mkdir -p $(REGISTRY_DATA)

start:	## start registry
	docker run -d --restart unless-stopped \
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

