
USR_BIN_DIR=/usr/bin
BIN_DIR=/wine/bin
SRC_DIR=/wine/tmp/docker
DOCKER_TAR=docker-20.10.20.tgz

pre-clean-yum:
	sudo yum remove docker-ce-crictl
	sudo yum remove docker-ce
	sudo yum remove containerd
	@echo
	sudo rpm -qa | grep docker

pre:
	mkdir -p ${BIN_DIR}
	mkdir -p ${SRC_DIR}

dl:
	curl -o ${SRC_DIR}/docker-conf.zip $(DFS_PUB_URL)/configs/docker/?zip
	curl -o ${SRC_DIR}/${DOCKER_TAR} $(DFS_PUB_URL)/pkgs/docker/${DOCKER_TAR}

untar:
	cd ${SRC_DIR}; unzip docker-conf.zip
	@echo
	cd ${SRC_DIR}; tar -xzvf ${DOCKER_TAR}
	@echo
	ls -alh ${SRC_DIR}

cp-bin:
	mkdir -p ${BIN_DIR}
	cp ${SRC_DIR}/docker/* ${BIN_DIR}/
	@echo
	ls -alh ${BIN_DIR}

ln:
	sudo ln -s ${BIN_DIR}/docker ${USR_BIN_DIR}/docker
	sudo ln -s ${BIN_DIR}/dockerd ${USR_BIN_DIR}/dockerd
	sudo ln -s ${BIN_DIR}/containerd ${USR_BIN_DIR}/containerd
	sudo ln -s ${BIN_DIR}/runc ${USR_BIN_DIR}/runc
	sudo ln -s ${BIN_DIR}/docker-proxy ${USR_BIN_DIR}/docker-proxy
	sudo ln -s ${BIN_DIR}/docker-init ${USR_BIN_DIR}/docker-init

cp-conf:
	sudo mkdir -p /etc/docker
	sudo cp ${SRC_DIR}/docker/daemon.json /etc/docker/

cp-svc:
	sudo cp ${SRC_DIR}/docker/docker.service /usr/lib/systemd/system/docker.service

enable:
	sudo systemctl enable docker.service
	sudo systemctl status docker.service | cat

restart:
	sudo systemctl daemon-reload
	sudo systemctl restart docker

stop:
	sudo systemctl stop docker

status:
	sudo systemctl status docker.service | cat
	@echo
	docker info

info: status

ls:
	ls -alh ${BIN_DIR}
	@echo
	ls -alh /etc/docker

clean-all:
	-sudo rm ${USR_BIN_DIR}/docker
	-sudo rm ${USR_BIN_DIR}/dockerd
	-sudo rm ${USR_BIN_DIR}/containerd
	-sudo rm ${USR_BIN_DIR}/runc
	-sudo rm ${USR_BIN_DIR}/docker-proxy
	-sudo rm ${USR_BIN_DIR}/docker-init
	@echo
	-sudo rm /usr/lib/systemd/system/docker.service
	-sudo rm /etc/docker/docker.service
