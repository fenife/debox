
#------------------------------------------------------------
# const
#------------------------------------------------------------
# DFS_URL=http://registry.dev.local:9060/data

DL_DIR=/wine/tmp/downloads
BAK_DIR=/wine/bak

#------------------------------------------------------------
# common
#------------------------------------------------------------
pre:
	mkdir -p $(DL_DIR)
	mkdir -p $(BAK_DIR)

define _ls_bak
	ls -alh $(BAK_DIR)
	@echo
	tree $(BAK_DIR)
endef

define _ls_dl
	ls -alh $(DL_DIR)
	@echo
	tree $(DL_DIR)
endef

define _echo_line
	@echo
	@echo '------------------------------------------------------------'
endef

ls:
	$(call _ls_dl)
	$(call _echo_line)
	$(call _ls_bak)


#------------------------------------------------------------
# /etc/hosts
#------------------------------------------------------------
HOST_BAK_DIR=$(BAK_DIR)/host

host-bak:
	mkdir -p $(HOST_BAK_DIR)
	cp /etc/hosts $(HOST_BAK_DIR)/ -rf
	@echo
	@ls -alh $(HOST_BAK_DIR)
	$(call _echo_line)

host-cat:
	$(call _echo_line)
	cat /etc/hosts
	$(call _echo_line)
	cat $(HOST_BAK_DIR)/hosts
	$(call _echo_line)
	-cat $(DL_DIR)/hosts

# 提前添加 registry 条目
host-add-reg: host-bak
	echo "192.168.2.160   registry.dev.local" | sudo tee -a /etc/hosts

# 下载文件指定目录
host-dl:
	curl -o $(DL_DIR)/hosts $(DFS_URL)/configs/host/hosts

# 添加 host 条目
host-add: host-bak host-dl
	cat $(DL_DIR)/hosts | sudo tee -a /etc/hosts
	
# 清除添加的 host 条目
# 备份原文件，再删除标记行及之后的行 (## user define host ##)
host-clear: host-bak
	sudo sed -i.bak '/^## user define host ##$$/,$$d' /etc/hosts

# 通过备份文件恢复
host-rb:
	sudo cp $(HOST_BAK_DIR)/hosts /etc/hosts

#------------------------------------------------------------
# bash
#------------------------------------------------------------
setup_bash:
	echo "source /wine/debox/share/rc/ext.bashrc" >> ${HOME}/.bashrc
	cp conf/.inputrc ${HOME}/

setup_vscode:
	mkdir -p ${HOME}/.ssh
	cat ssh/id_rsa_feng.pub >> ${HOME}/.ssh/authorized_keys
	chmod 600 ${HOME}/.ssh/auth_keys
	chmod 700 ${HOME}/.ssh

setup_git:
	cp conf/.gitconfig ${HOME}/

setup_pip:
	mkdir -p ${HOME}/.pip
	cp conf/pip.conf ${HOME}/.pip
	@echo
	ls ${HOME}/.pip

setup_zsh:
	sudo yum install zsh
	sudo usermod -s /usr/bin/zsh $USER

tmp_dir = /tmp
setup_ohmyzsh:
	curl -O ohmyzsh.zip /tmp
	cd /tmp; unzip -q ohmyzsh.zip
	mv /tmp/ohmyzsh-master ${HOME}/.oh-my-zsh
	cp ${HOME}/.oh-my-zsh/templates/zshrc.zsh-template ${HOME}/.zshrc
	echo "source /wine/debox/share/rc/ext.zshrc" >> ${HOME}/.zshrc
	sed -i "s/robbyrussell/ys/" ${HOME}/.zshrc

