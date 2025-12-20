
BASE_DIR=/wine
CUR_DIR := $(shell pwd)

DL_DIR=${BASE_DIR}/tmp/downloads/host
BAK_DIR=${BASE_DIR}/bak/host

DFS_PUB_URL=http://local.dfs.io:9060/files
DFS_PRIV_URL=http://local.dfs.io:9060/files

.PHONY: help h pre ls bak cat dl add clear rb  # 声明伪目标

help:		## help
	@echo "usage:"
	@echo "  cur dir:       ${CUR_DIR}"
	@echo "  download dir:  ${DL_DIR}"
	@echo "  backup dir:    ${BAK_DIR}"
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
	ls -alh $(1)
	@echo
	tree $(1)
endef

#------------------------------------------------------------
# cmd
#------------------------------------------------------------

pre:		## prepare
	mkdir -p ${DL_DIR}	
	@echo
	mkdir -p ${BAK_DIR}	

ls:			## ls dir
	$(call _ls_dir,${DL_DIR})
	$(call _echo_line)
	$(call _ls_dir,${BAK_DIR})

bak:		## backup hosts
	mkdir -p ${BAK_DIR}
	cp /etc/hosts ${BAK_DIR}/ -rf
	@echo
	@ls -alh ${BAK_DIR}
	$(call _echo_line)

cat:		## cat hosts
	$(call _echo_line)
	@echo "=== 当前系统 /etc/hosts ==="
	cat /etc/hosts
	$(call _echo_line)
	@echo "=== 备份的 hosts 文件 ==="
	cat ${BAK_DIR}/hosts
	$(call _echo_line)
	@echo "=== 待添加的 hosts 文件 ${DL_DIR} ==="
	-cat ${DL_DIR}/hosts

# 提前添加 DFS 条目
add-dfs: bak		## add dfs hosts first
	echo "\n## user define host ##" | sudo tee -a /etc/hosts
	echo "192.168.2.160   local.dfs.io" | sudo tee -a /etc/hosts

# 下载文件指定目录
dl:		## download hosts
	curl -o ${DL_DIR}/hosts ${DFS_PRIV_URL}/configs/etc/hosts

# 添加 host 条目
add: bak		## add hosts
	@echo "=== 追加下载的 hosts 到 /etc/hosts ==="
	cat ${DL_DIR}/hosts | sudo tee -a /etc/hosts
	
# 清除添加的 host 条目
# 备份原文件，再删除标记行及之后的行 (## user define host ##)
clear: bak		## clear user define host
	@echo "=== 清除自定义 hosts 条目 (标记：## user define host ##) ==="
	sudo sed -i.bak '/^## user define host ##$$/,$$d' /etc/hosts

# 通过备份文件恢复
rb:			## rollback
	@echo "=== 从 $(BAK_DIR)/hosts 恢复 /etc/hosts ==="
	sudo cp ${BAK_DIR}/hosts /etc/hosts
