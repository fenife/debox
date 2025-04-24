
include $(INC_DIR)/Makefile.inc

ETCD_IMAGE=$(REGISTRY_URL)/bitnami/etcd:3.5
ETCD_NAME=etcd-3.5
ETCD_DATA_DIR=/wine/var/etcd

.PHONY: start stop

pull:
	docker pull $(ETCD_IMAGE)

start:
	mkdir -p $(ETCD_DATA_DIR)

	docker run -d --name $(ETCD_NAME) \
	--publish 2379:2379 \
	--publish 2380:2380 \
	-v $(ETCD_DATA_DIR):/bitnami/etcd \
	--env ALLOW_NONE_AUTHENTICATION=yes \
	--env ETCD_ADVERTISE_CLIENT_URLS=http://$(ETCD_NAME):2379 \
	$(ETCD_IMAGE)

stop:
	docker stop $(ETCD_NAME)
	docker rm $(ETCD_NAME)

enter:
	docker exec -it $(ETCD_NAME) bash


# see: https://github.com/etcd-io/etcd/releases/tag/v3.4.32
# start:
# 	docker run -d -p 2379:2379 -p 2380:2380 \
# 	--name $(ETCD_NAME) \
# 	-v $(ETCD_DATA_DIR):/etcd-data \
#   	$(ETCD_IMAGE) \
# 	/usr/local/bin/etcd \
# 	--name etcd0 \
# 	--data-dir /etcd-data \
# 	--listen-client-urls http://0.0.0.0:2379 \
# 	--advertise-client-urls http://0.0.0.0:2379 \
# 	--listen-peer-urls http://0.0.0.0:2380 \
# 	--initial-advertise-peer-urls http://0.0.0.0:2380 \
# 	--initial-cluster etcd0=http://0.0.0.0:2380 \
# 	--initial-cluster-token tkn \
# 	--initial-cluster-state new \
# 	--log-level info \
# 	--logger zap 

