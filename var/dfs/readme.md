
## 说明
drive: 驱动器，比如磁盘驱动器的意思

## 目录结构
files
    configs      # 配置文件，提交到git
        os
            centos7
            ubuntu22
        etc
            hosts
        home
            .gitconfig
            pip.conf
        vscode
        docker

    pkgs         # 下载的安装包等，不提交到git
        go
        docker
        kind

    images      # docker 容器镜像包，不提交到git
