# debox

some tools and project examples for development.

## 名词
- runc: run about container
- runs: run about service

- rinh: run in host
- rinc: run in container(docker)
- rind: run in docker(container)
- rinv: run in vm  (docker in docker)

- rinp: run in pod (docker, container)


- stable: 稳定版
- release: 发布

- hub: 中心
- public: 公共
- private: 私有
- repo: repository, 仓库
- lab: laboratory, 实验
- app: application, 应用

## layer
- layer1: base
- layer2: testc
- layer3: packages
- layer4: builder
- layer5: ovs
- layer6: vscode
- layery: config

## webui
- shell: multi cmd
- netns: network namespace 

## dir
```text

wine

debox
    build
        image
            alpine
            centos7
            rhel8  
                dev
                local
            python
                dev
                    python3.12-rhel8.4
            golang
        etc
            conf
                git
                ssh
                pip
            yum
                centos7
                rhel8
        repo    (public repo)
            src
                python 
            linux  
                etcd
            alpine
                apk
            centos7
                ovs
            rhel8 
                ovs
            vscode
    local
        infra
            mysql
            redis
    share
        iapp
        ilab
        app
        bin
        include
        rc
        work
        tmp
```
