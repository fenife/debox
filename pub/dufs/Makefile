# source: https://github.com/sigoden/dufs

include $(INC_DIR)/Makefile.inc

DUFS_IMAGE = $(REGISTRY_URL)/sigoden/dufs:v0.42.0
DUFS_NAME = dufs-0.42
DUFS_PORT = 8800
DUFS_DATA = /wine/debox/pub/drive

pre:	## prepare
	mkdir -p $(DUFS_DATA)

start:	## start registry
	docker run -d --restart on-failure:3 \
	--name $(DUFS_NAME) \
	-p $(DUFS_PORT):5000 \
	-v $(DUFS_DATA):/data \
	-e DUFS_ALLOW_ALL=false \
	-e DUFS_ALLOW_ARCHIVE=true \
	-e DUFS_ALLOW_SEARCH=true \
	$(DUFS_IMAGE) \
	/data 

stop:		## stop registry
	docker stop $(DUFS_NAME)

rm:			## rm registry
	docker rm $(DUFS_NAME)

restart:
	docker restart $(DUFS_NAME)


