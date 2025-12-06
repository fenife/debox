
## 前置
### 镜像
```bash
local.registry.io:9000/sigoden/dufs:v0.42.0
local.registry.io:9000/library/registry:2.8
local.registry.io:9000/joxit/docker-registry-ui:2.5.7
```

## 目录说明
public
    srv             # 公共服务
        dufs
        registry
        registry_ui
    infra           # 基础服务
        mysql
        redis
        etcd
    var             # 服务数据目录
        dfs         # vscode 可见的数据目录
            files
                configs
                images
                pkgs
        lib         # vscode 可隐藏的数据目录，避免展示的文件太多
            registry
            mysql
            redis
            etcd
    etc
        hosts
            local.dfs.io
            local.registry.io
            dev.dfs.io
            dev.registry.io
        envs
            export DFS_PUB_URL=local.dfs.io
            export DFS_PRIV_URL=local.dfs.io
            export REGISTRY_URL=local.registry.io

