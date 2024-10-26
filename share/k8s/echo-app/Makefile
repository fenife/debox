
include $(INC_DIR)/Makefile.common

ECHO_APP_IMAGE=echo-app:latest
REGISTER_ECHO_APP_IMAGE=register.dev.local:5000/echo-app:latest
ECHO_APP_NAME=echo-app
CLUSTER_NAME=local

############################################################
# echo-app docker 
############################################################

build: 	## docker build image
	docker build -t $(ECHO_APP_IMAGE) ./echo-go

start: 	## docker start echo-app
	docker run --rm -it \
	--name $(ECHO_APP_NAME) --hostname $(ECHO_APP_NAME) \
	-p 6000:6000 \
	$(ECHO_APP_NAME)

stop:	## docker stop echo-app
	docker stop $(ECHO_APP_NAME)
	docker rm $(ECHO_APP_NAME)

enter:	## docker attach echo-app container
	docker exec -it $(ECHO_APP_NAME) bash

tag:		## tag image 
	docker tag $(ECHO_APP_IMAGE) $(REGISTER_ECHO_APP_IMAGE)

# kind load docker-image $(REGISTER_ECHO_APP_IMAGE) --name $(CLUSTER_NAME)
load: 	## load image to kind
	kind load docker-image $(ECHO_APP_IMAGE) --name $(CLUSTER_NAME)

push: tag		## push image to local registry
	docker push $(REGISTER_ECHO_APP_IMAGE)

############################################################
# echo-app k8s
############################################################

start-pod:		## start pod
	kubectl apply -f ./yaml/rs.yaml

stop-pod:		## stop pod
	kubectl delete -f ./yaml/rs.yaml

start-svc:		## start svc
	kubectl apply -f ./yaml/svc.yaml

stop-svc:		## stop svc
	kubectl delete -f ./yaml/svc.yaml

start-np:		## start svc nodeport
	kubectl apply -f ./yaml/svc-nodeport.yaml

stop-np:		## stop svc nodeport
	kubectl delete -f ./yaml/svc-nodeport.yaml

start-lb:		## start svc loadbalancer
	kubectl apply -f ./yaml/svc-lb.yaml

stop-lb:		## stop svc loadbalancer
	kubectl delete -f ./yaml/svc-lb.yaml

start-ing:		## start ingress
	kubectl apply -f ./yaml/svc-ingress.yaml

stop-ing:		## stop ingress
	kubectl delete -f ./yaml/svc-ingress.yaml

start-deploy:		## start deployment
	kubectl apply -f ./yaml/deploy.yaml

stop-deploy:		## stop deployment
	kubectl delete -f ./yaml/deploy.yaml

start-all: load start-pod start-svc start-np start-lb ## start all 

clean-all: stop-pod stop-svc stop-np stop-lb	## clean all

############################################################
# pod runtime
############################################################
NODE := local-worker
POD := echo-app-9vjv9
SVC_IP := 10.96.167.207
SVC_DNS := echo-svc.default

NODE_EXEC := docker exec -it $(NODE)
POD_EXEC := kubectl exec $(POD) --

atw:	## attach worker node
	docker exec -it $(NODE) bash

atp:	## attach pod
	kubectl exec -it $(POD) bash

ping1:	## curl service ip from node
	$(NODE_EXEC) curl -s http://$(SVC_IP):6000

# see: file in pod: /etc/resolv.conf
ping2: 		## curl service dns name from pod
	$(POD_EXEC) cat /etc/resolv.conf
	@echo
	$(POD_EXEC) curl -s http://$(SVC_DNS):6000

ping3: 		## service nodeport
	$(NODE_EXEC) curl -s http://127.0.0.1:30006

ping4: 		## localhost and nodeport
	curl -s http://127.0.0.1:30006

ping5: 		## localhost and loadbalancer
	curl -s http://127.0.0.1:30008

# 域名在 /etc/hosts 中配置
ping6: 		## ingress
	curl http://echo.dev.local:10080
