
CUR_DIR := $(shell pwd)
BASE_DIR=/wine
USR_BIN_DIR=/usr/bin
BIN_DIR=${BASE_DIR}/bin
DL_DIR=${BASE_DIR}/tmp/downloads/dockers
DOCKER_TAR=docker-20.10.20.tgz

RC_DIR=${BASE_DIR}/debox/share/rc/

DFS_PUB_URL=http://local.dfs.io:9060/files
DFS_PRIV_URL=http://local.dfs.io:9060/files

.PHONY: help h pre

help: 	## help
	@echo "usage:"
	@echo "  cur dir:       ${CUR_DIR}"
	@echo "  bin dir:       ${BIN_DIR}"
	@echo "  download dir:  ${DL_DIR}"
	@echo "  rc dir:        ${RC_DIR}"
	@echo "  docker file:   ${DOCKER_TAR}"
	@echo "  dfs pub url:   ${DFS_PUB_URL}"
	@echo "  dfs priv url:  ${DFS_PRIV_URL}"
	@echo
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s \033[0m%s\n", $$1, $$2}'

	@echo

h: help		## help

#------------------------------------------------------------
# function
#------------------------------------------------------------

define _echo_line
	@echo
	@echo '------------------------------------------------------------'
endef

define _ls_dir
	$(call _echo_line)
	ls -alh $(1)
	@echo
	tree -a $(1)
endef


#------------------------------------------------------------
# prepare
#------------------------------------------------------------

pre:		## prepare
	mkdir -p ${DL_DIR}	
	mkdir -p ${BIN_DIR}

ls:		## ls dir
	$(call _ls_dir,${DL_DIR})
	$(call _ls_dir,${BIN_DIR})
	$(call _ls_dir,/etc/docker)

dl: pre		## download
	curl -o ${DL_DIR}/docker-conf.zip $(DFS_PUB_URL)/configs/docker/?zip
	curl -o ${DL_DIR}/${DOCKER_TAR} $(DFS_PUB_URL)/pkgs/docker/${DOCKER_TAR}

unzip:		## unzip
	cd ${DL_DIR}; unzip docker-conf.zip
	@echo
	cd ${DL_DIR}; tar -xzvf ${DOCKER_TAR}
	@echo
	ls -alh ${DL_DIR}

dl-clean:		## download clean
	rm -rf ${DL_DIR}

#------------------------------------------------------------
# setup
#------------------------------------------------------------

pre-clean-yum:		## pre clean yum
	sudo yum remove docker-ce-crictl
	sudo yum remove docker-ce
	sudo yum remove containerd
	@echo
	sudo rpm -qa | grep docker

cp-bin:			## cp bin
	cp ${DL_DIR}/docker/* ${BIN_DIR}/
	@echo
	ls -alh ${BIN_DIR}

ln:		## ln
	sudo ln -s ${BIN_DIR}/docker ${USR_BIN_DIR}/docker
	sudo ln -s ${BIN_DIR}/dockerd ${USR_BIN_DIR}/dockerd
	sudo ln -s ${BIN_DIR}/containerd ${USR_BIN_DIR}/containerd
	sudo ln -s ${BIN_DIR}/runc ${USR_BIN_DIR}/runc
	sudo ln -s ${BIN_DIR}/docker-proxy ${USR_BIN_DIR}/docker-proxy
	sudo ln -s ${BIN_DIR}/docker-init ${USR_BIN_DIR}/docker-init

cp-conf:		## copy config
	sudo mkdir -p /etc/docker
	sudo cp ${DL_DIR}/daemon.json /etc/docker/

cat-conf:		## cat config
	cat /etc/docker/daemon.json

cp-svc:			## copy service
	sudo cp ${DL_DIR}/docker.service /usr/lib/systemd/system/docker.service

cat-svc:		## cat service
	cat /usr/lib/systemd/system/docker.service

add-group:		## add docker group
	sudo groupadd docker

enable:			## enable service
	sudo systemctl enable docker.service
	@echo
	sudo systemctl status docker.service | cat

restart:		## restart
	sudo systemctl daemon-reload
	sudo systemctl restart docker

stop:			## stop
	sudo systemctl stop docker

status:			## status
	sudo systemctl status docker.service | cat
	@echo
	docker info

usermod:		## add user to docker group
	sudo usermod -aG docker ${USER}
	groups ${USER}

clean-all:		## clean all
	-sudo rm ${USR_BIN_DIR}/docker
	-sudo rm ${USR_BIN_DIR}/dockerd
	-sudo rm ${USR_BIN_DIR}/containerd
	-sudo rm ${USR_BIN_DIR}/runc
	-sudo rm ${USR_BIN_DIR}/docker-proxy
	-sudo rm ${USR_BIN_DIR}/docker-init
	@echo
	-sudo rm /usr/lib/systemd/system/docker.service
	-sudo rm /etc/docker/daemon.json
