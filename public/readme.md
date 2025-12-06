

## 前置
```bash
# 导出 PUB_DIR 目录
export PUB_DIR=path_to_pub
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
    envs
        local.dfs.io
        dev.dfs.io
        local.registry.io
        dev.registry.io

        export DFS_PUB_URL
        export DFS_PRIV_URL
        export REGISTRY_URL

    local
        hosts
        envs
    dev
        hosts
        envs
            DFS_URL
            REGISTRY_URL

