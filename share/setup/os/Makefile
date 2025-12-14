
BASE_DIR=/wine
CUR_DIR := $(shell pwd)

DL_DIR=${BASE_DIR}/tmp/downloads/configs
BAK_DIR=${BASE_DIR}/bak/configs
RC_DIR=${BASE_DIR}/debox/share/rc/

DFS_PUB_URL=http://local.dfs.io:9060/files
DFS_PRIV_URL=http://local.dfs.io:9060/files

.PHONY: help h pre

help:	## help
	@echo "usage:"
	@echo "  cur dir:       ${CUR_DIR}"
	@echo "  download dir:  ${DL_DIR}"
	@echo "  backup dir:    ${BAK_DIR}"
	@echo "  rc dir:        ${RC_DIR}"
	@echo "  dfs pub url:   ${DFS_PUB_URL}"
	@echo "  dfs priv url:  ${DFS_PRIV_URL}"
	@echo
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s \033[0m%s\n", $$1, $$2}'

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

pre:	## pre
	mkdir -p ${DL_DIR}	
	@echo
	mkdir -p ${BAK_DIR}	

ls:
	$(call _ls_dir,${DL_DIR})
	$(call _ls_dir,${BAK_DIR})

dl: pre
	curl -o ${DL_DIR}/configs.zip ${DFS_PRIV_URL}/configs/home/?zip
	@echo
	curl -o ${DL_DIR}/ohmyzsh.zip ${DFS_PUB_URL}/pkgs/zsh/ohmyzsh-master.zip

unzip:
	cd ${DL_DIR}; unzip ${DL_DIR}/configs.zip

dl-clean:
	rm -rf ${DL_DIR}

#------------------------------------------------------------
# setup
#------------------------------------------------------------

setup-bash:
	echo "source ${RC_DIR}/ext.bashrc" >> ${HOME}/.bashrc
	cp ${DL_DIR}/.inputrc ${HOME}/

setup-vscode:
	mkdir -p ${HOME}/.ssh
	cat ${DL_DIR}/ssh/id_rsa_feng.pub >> ${HOME}/.ssh/authorized_keys
	chmod 600 ${HOME}/.ssh/auth_keys
	chmod 700 ${HOME}/.ssh

setup-git:
	cp ${DL_DIR}/.gitconfig ${HOME}/

setup-pip:
	mkdir -p ${HOME}/.pip
	cp ${DL_DIR}/pip.conf ${HOME}/.pip
	@echo
	ls ${HOME}/.pip

setup-zsh-yum:
	sudo yum install zsh
	sudo usermod -s /usr/bin/zsh $USER

setup-zsh-apt:
	sudo apt install zsh
	sudo usermod -s /usr/bin/zsh $USER

setup-ohmyzsh:
	cd ${DL_DIR}; unzip -q ${DL_DIR}/ohmyzsh.zip
	mv ${DL_DIR}/ohmyzsh-master ${HOME}/.oh-my-zsh
	cp ${HOME}/.oh-my-zsh/templates/zshrc.zsh-template ${HOME}/.zshrc
	echo "\nsource ${RC_DIR}/ext.zshrc\n" | tee -a ${HOME}/.zshrc
	sed -i "s/robbyrussell/ys/" ${HOME}/.zshrc

# robbyrussell, ys, crcandy
setup-zsh-theme:
	sed -i '/^ZSH_THEME=/c\\ZSH_THEME="crcandy"' ~/.zshrc

rm-ohmyzsh:
	rm -rf ${HOME}/.oh-my-zsh

proxy:
	export HTTP_PROXY=http://feng-win:7890
	export HTTPS_PROXY=http://feng-win:7890
	export ALL_PROXY=socks5://feng-win:7890

noproxy:
	export HTTP_PROXY=
	export HTTPS_PROXY=
	export ALL_PROXY=
