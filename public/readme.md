

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
        registry
        mysql
        redis
        etcd
        dfs
            files
                configs
                images
                pkgs
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

