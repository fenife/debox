# source: https://github.com/sigoden/dufs

include $(INC_DIR)/Makefile.inc

DUFS_NAME = dufs-0.42
DUFS_IMAGE = $(REGISTRY_URL)/sigoden/dufs:v0.42.0
DUFS_PORT = 8800
DUFS_DATA = /wine/var/dufs

pre:	## prepare
	mkdir -p $(DUFS_DATA)

start:	## start registry
	docker run -d --restart on-failure:3 \
	--name $(DUFS_NAME) \
	-p $(DUFS_PORT):5000 \
	-v $(DUFS_DATA):/data \
	$(DUFS_IMAGE) \
	/data -A

stop:		## stop registry
	docker stop $(DUFS_NAME)

rm:			## rm registry
	docker rm $(DUFS_NAME)

restart:
	docker restart $(DUFS_NAME)

check:		## check registry
	curl http://$(REGISTRY_URL)/v2/_catalog

