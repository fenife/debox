
include $(INC_DIR)/Makefile.common

CLUSTER_NAME=local

start:	## start cluster
	kind create cluster --config=cluster.yaml

stop:	## stop cluster
	kind delete cluster -n $(CLUSTER_NAME)

atc:	## attach control plane
	docker exec -it local-control-plane /bin/bash

at1:	## attach worker1
	docker exec -it local-worker /bin/bash

at2:	## attach worker2
	docker exec -it local-worker2 /bin/bash

ctx:	## kubectl context
	kubectl cluster-info --context kind-$(CLUSTER_NAME)

ver:	## kubectl version
	kubectl version

info:	## cluster info
	kubectl cluster-info
	@echo
	kubectl get nodes -o wide
	@echo
	kubectl get pods -o wide --all-namespaces
	@echo
	kubectl get svc -o wide --all-namespaces
	@echo
	kubectl get endpoints -o wide --all-namespaces
	@echo
	kubectl get ingress -o wide --all-namespaces
	@echo
	kubectl get secret -o wide --all-namespaces

image:		## worker image ls
	docker exec -it local-worker crictl images

start-registry:			## start docker registry
	docker run -d \
	--name docker-registry \
	--restart=always  \
	-v /wine/k8s/registry:/var/lib/registry \
	-p 5000:5000 \
	registry:2.8

stop-registry:	## stop docker registry
	docker stop docker-registry
	docker rm docker-registry






