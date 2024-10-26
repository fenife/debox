FROM centos:8.4.2105

# 时区
ENV TZ "Asia/Shanghai"
# 禁用交互式提示
ENV DEBIAN_FRONTEND noninteractive
# 设置编码，解决zsh下中文乱码问题
# ENV LANG=en_US.UTF-8
# ENV LC_ALL=en_US.UTF-8
# ENV LC_CTYPE=en_US.UTF-8
# terminal colors with xterm
ENV TERM xterm
# home dir
ENV HOME_DIR /root

############################################################
# install base softwares
############################################################

# repo
RUN rm -rf /etc/yum.repo.d/*
ADD repo/*.repo /etc/yum.repos.d/

# fix:  Could not open/read file:///etc/pki/rpm-gpg/RPM-GPG-KEY-puias
ADD pkg/libmodulemd-*.rpm /tmp
RUN yum install -y /tmp/libmodulemd-*.rpm

# 基础工具下载
RUN yum install -y curl wget tar bzip2 unzip vim passwd sudo tree rsync man git tig tmux \
    # 编译
    gcc gcc-c++ make yum-utils automake cmake autoconf rpm-build redhat-rpm-config \
    # 网络
    iptables ipset iproute hostname net-tools telnet nc tcpdump bridge-utils traceroute \
    # 性能
    htop psmisc sysstat strace lsof \
    # 其他组件
    mysql redis openssh-server util-linux-user \
    # 依赖
    zlib libffi libtool python3-devel libpng-devel libjpeg-devel openssl-devel mysql-devel \
    zlib-devel libffi-devel bzip2-devel sqlite-devel readline-devel tk-devel \
    perl-ExtUtils-MakeMaker ncurses-devel curl-devel expat-devel gettext-devel \
    kernel-devel kernel-debug-devel \
    # dind
    supervisor NetworkManager python3-setuptools iptables-services \
    # --nogpgcheck
    && yum clean all

# # install openssl
# COPY pkg/openssl-1.1.1w.tar.gz /tmp/
# RUN cd /tmp/ \
#     && tar -xzf openssl-1.1.1w.tar.gz \
#     && cd openssl-1.1.1w  \
#     && ./config --prefix=/usr \
#     && make \
#     && make install_sw install_ssldirs \
#     && rm -rf /tmp/openssl-*

# zsh
# 安装zsh，默认安装在：/usr/local/bin/zsh
# 参考：https://blog.csdn.net/u012605514/article/details/121797773
COPY zsh/zsh-5.8.tar.xz /tmp/
RUN cd /tmp \
    && tar -xf zsh-5.8.tar.xz \
    && cd zsh-5.8 \
    && ./configure --without-tcsetpgrp \
    && make \
    && make install \
    && rm -rf /tmp/zsh-* 
RUN ln -s $(which zsh) /bin/zsh \
    && echo "/bin/zsh" >> /etc/shells

# 安装 oh my zsh 
COPY zsh/ohmyzsh-master.zip /tmp/
RUN cd /tmp \
    && unzip -q ohmyzsh-master.zip \
    && mv ohmyzsh-master ${HOME_DIR}/.oh-my-zsh \
    && cp ${HOME_DIR}/.oh-my-zsh/templates/zshrc.zsh-template ${HOME_DIR}/.zshrc \
    && rm -rf /tmp/ohmyzsh-*

# install python3.12 with ssl
COPY pkg/Python-3.12.0.tgz /tmp/
RUN cd /tmp/ \
    && tar -xzf Python-3.12.0.tgz \
    && cd Python-3.12.0 \
    && ./configure --prefix=/usr/local/python3.12 --with-ssl \
    && make \
    && make install \
    && rm -rf /tmp/Python-*

# 安装 golang 
RUN cd /tmp \
    && wget https://golang.google.cn/dl/go1.22.3.linux-amd64.tar.gz \
    && tar -zxf go1.22.3.linux-amd64.tar.gz -C /usr/local \
    && rm -rf /tmp/go*
ENV PATH="$PATH:/usr/local/go/bin"

# install golang dlv gopls staticcheck
RUN go env -w GOPROXY=https://goproxy.cn,direct \
    && go env -w GO111MODULE=on \
    && go env -w GOSUMDB='off'
RUN go install golang.org/x/tools/gopls@v0.15.3 \
    && go install github.com/go-delve/delve/cmd/dlv@v1.22.1 \
    && go install honnef.co/go/tools/cmd/staticcheck@v0.4.7 

# 安装vscode
# 对应以下版本：
#   版本: 1.89.1 (user setup)
#   提交: dc96b837cf6bb4af9cd736aa3af08cf8279f7685
#   日期: 2024-05-07T05:13:33.891Z
ENV VSCODE_ID=dc96b837cf6bb4af9cd736aa3af08cf8279f7685
ENV VSCODE_BIN_DIR=${HOME_DIR}/.vscode-server/bin/${VSCODE_ID}
COPY vscode/vscode-server-linux-x64-*.tar.gz /tmp/
RUN mkdir -p ${VSCODE_BIN_DIR} \
    && tar -xzf /tmp/vscode-server-linux-x64-*.tar.gz -C ${VSCODE_BIN_DIR} --strip 1 \
    && rm /tmp/vscode-*

# 安装 vscode extensions
COPY vscode/ext/* /tmp/vscode/ext/
ENV VSCODE_BIN=${VSCODE_BIN_DIR}/bin/code-server
RUN cd /tmp/vscode/ext/ \
    # 传入 code-server 执行文件的路径，在脚本里遍历安装扩展文件
    && ./install.sh ${VSCODE_BIN}

############################################################
# install modules and plugins
############################################################
# ENV PATH="$PATH:/usr/local/python3.12/bin"

############################################################
# configs
############################################################

# zsh config
# 自动补全
ENV ZSH_CUSTOM=${HOME_DIR}/.oh-my-zsh/custom
# RUN mkdir -p ${ZSH_CUSTOM}/plugins/incr
COPY zsh/incr-0.2.zsh ${ZSH_CUSTOM}/plugins/incr/incr.zsh
# zshr配置
COPY zsh/ext.zsh /tmp/ 
RUN cat /tmp/ext.zsh >> ${HOME_DIR}/.zshrc \
    && rm -rf /tmp/*.zsh \
    # 设置主题
    && sed -i "s/robbyrussell/ys/" ${HOME_DIR}/.zshrc 
# 切换shell
RUN chsh -s /bin/zsh 

# git config
COPY conf/.gitconfig /${HOME_DIR}/.gitconfig

# python config
COPY conf/pip.conf ${HOME_DIR}/.pip/pip.conf

# 配置ssh 
# RUN sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/g' /etc/ssh/sshd_config
# RUN sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/g' /etc/ssh/sshd_config
# Docker服务器开放的端口，供容器外部连接使用(在启动容器时做端口映射)
# EXPOSE 22   

# install openvswitch
# see: https://blog.csdn.net/weixin_42072280/article/details/119764004
# RUN yum install -y epel-release \
RUN yum install -y centos-release-openstack-train openvswitch libibverbs \
    && yum clean all 

# install docker for dind
# https://download.docker.com/linux/static/stable/x86_64/docker-19.03.0.tgz
COPY docker/docker-19.03.0.tgz /tmp/docker/
RUN set -eux; \
    cd /tmp/docker/ \
    && tar -xzf docker-19.03.0.tgz --strip-components 1 -C /usr/local/bin \
    && rm -rf /tmp/docker
# install docker compose
# https://github.com/docker/compose/releases/download/v2.22.0/docker-compose-linux-x86_64
COPY docker/docker-compose-Linux-x86_64 /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose 
COPY docker/daemon.json /etc/docker/

# install supervisor
COPY supervisor/* /etc/supervisord.d/

# install cmd
COPY cmd/* /wine/bin/
RUN chmod +x /wine/bin/*.sh
ENV PATH="$PATH:/wine/bin"

# ENV PATH="$PATH:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin"

WORKDIR /wine

# CMD [ "start.sh" ]
CMD ["/bin/zsh"]

