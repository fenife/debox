
include $(INC_DIR)/Makefile.common

REDIS_IMAGE=redis:7.0
REDIS_NAME=redis
REDIS_DATA_DIR=$(ROOT_DIR)/var/redis

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

