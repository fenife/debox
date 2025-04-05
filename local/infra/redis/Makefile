
include $(INC_DIR)/Makefile.inc

REDIS_IMAGE=$(REGISTRY_URL)/redis:7.0
REDIS_NAME=redis7.0
REDIS_DATA_DIR=/wine/var/redis

.PHONY: start stop

pull:
	docker pull $(REDIS_IMAGE)

start:
	docker run -d -p 6379:6379 --name $(REDIS_NAME) \
	-v $(REDIS_DATA_DIR):/data \
	$(REDIS_IMAGE) 

stop:
	docker stop $(REDIS_NAME)
	docker rm $(REDIS_NAME)

enter:
	docker exec -it $(REDIS_NAME) bash

