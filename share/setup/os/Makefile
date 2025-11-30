
#------------------------------------------------------------
# const
#------------------------------------------------------------
DFS_DATA_URL=http://registry.dev.local:9060/data

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
	curl -o $(DL_DIR)/hosts $(DFS_DATA_URL)/configs/host/hosts

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

