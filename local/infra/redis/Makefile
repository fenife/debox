
include $(INC_DIR)/Makefile.inc

REDIS_IMAGE=$(REGISTRY_URL)/redis:7.0
REDIS_NAME=redis7.0
REDIS_DATA_DIR=/wine/var/redis

.PHONY: start stop

pre:
	mkdir -p $(REDIS_DATA_DIR)

pull:
	docker pull $(REDIS_IMAGE)

start:
	docker run -d --restart on-failure:3 \
	--name $(REDIS_NAME) \
	-p 6379:6379 \
	-v $(REDIS_DATA_DIR):/data \
	$(REDIS_IMAGE) 

stop:
	docker stop $(REDIS_NAME)
	docker rm $(REDIS_NAME)

enter:
	docker exec -it $(REDIS_NAME) bash

