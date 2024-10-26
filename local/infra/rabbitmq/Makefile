
include $(INC_DIR)/Makefile.common

RABBITMQ_IMAGE=rabbitmq:3.12-management
RABBITMQ_NAME=rabbitmq
RABBITMQ_DATA_DIR=$(ROOT_DIR)/var/rabbitmq
RABBITMQ_ROOT_PASSWORD=root

# docker pull $(RABBITMQ_IMAGE)
pull:
	docker pull m.daocloud.io/docker.io/$(RABBITMQ_IMAGE)
	docker tag m.daocloud.io/docker.io/$(RABBITMQ_IMAGE) $(RABBITMQ_IMAGE)

start:	## start
	docker run -d \
	-p 5672:5672 -p 15672:15672  \
	--name $(RABBITMQ_NAME) \
	-v $(RABBITMQ_DATA_DIR):/var/lib/rabbitmq \
	-e RABBITMQ_DEFAULT_USER=test \
	-e RABBITMQ_DEFAULT_PASS=test \
	-e RABBITMQ_DEFAULT_VHOST=test \
	$(RABBITMQ_IMAGE) 

stop:	## stop
	docker stop $(RABBITMQ_NAME)
	docker rm $(RABBITMQ_NAME)

restart:	## restart 
	docker restart $(RABBITMQ_NAME)

enter:	## attach
	docker exec -it $(RABBITMQ_NAME) bash

