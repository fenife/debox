
BASE_DIR=/wine
CUR_DIR := $(shell pwd)

DL_DIR=${BASE_DIR}/tmp/downloads/host
BAK_DIR=${BASE_DIR}/bak/host

DFS_PUB_URL=http://local.dfs.io:9060/files
DFS_PRIV_URL=http://local.dfs.io:9060/files

.PHONY: help h pre ls bak cat dl add clear rb  # 声明伪目标

help:
	@echo "usage:"
	@echo "  cur dir:       ${CUR_DIR}"
	@echo "  download dir:  ${DL_DIR}"
	@echo "  backup dir:    ${BAK_DIR}"
	@echo
	@echo "  pre          - 准备目录"
	@echo "  ls           - 查看目录"
	@echo "  bak          - 备份 hosts"
	@echo "  cat          - 查看 hosts"
	@echo "  add-dfs      - 提前添加 DFS 条目"
	@echo "  dl           - 下载 hosts 配置"
	@echo "  add          - 添加 host 条目"
	@echo "  clear        - 清除添加的 host 条目"
	@echo "  rb           - 通过备份文件恢复 hosts"
	@echo

h: help

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

pre:
	mkdir -p ${DL_DIR}	
	@echo
	mkdir -p ${BAK_DIR}	

ls:
	$(call _ls_dir,${DL_DIR})
	$(call _echo_line)
	$(call _ls_dir,${BAK_DIR})

bak:
	mkdir -p ${BAK_DIR}
	cp /etc/hosts ${BAK_DIR}/ -rf
	@echo
	@ls -alh ${BAK_DIR}
	$(call _echo_line)

cat:
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
add-dfs: bak
	echo "\n## user define host ##" | sudo tee -a /etc/hosts
	echo "192.168.2.160   local.dfs.io" | sudo tee -a /etc/hosts

# 下载文件指定目录
dl:
	curl -o ${DL_DIR}/hosts ${DFS_PRIV_URL}/configs/etc/hosts

# 添加 host 条目
add: bak
	@echo "=== 追加下载的 hosts 到 /etc/hosts ==="
	cat ${DL_DIR}/hosts | sudo tee -a /etc/hosts
	
# 清除添加的 host 条目
# 备份原文件，再删除标记行及之后的行 (## user define host ##)
clear: bak
	@echo "=== 清除自定义 hosts 条目 (标记：## user define host ##) ==="
	sudo sed -i.bak '/^## user define host ##$$/,$$d' /etc/hosts

# 通过备份文件恢复
rb:
	@echo "=== 从 $(BAK_DIR)/hosts 恢复 /etc/hosts ==="
	sudo cp ${BAK_DIR}/hosts /etc/hosts
