FROM local.registry.io:9000/library/ubuntu:22.04

#------------------------------------------------------------
# repo and base softwares
RUN mv /etc/apt/sources.list /tmp/ 
COPY configs/os/ubuntu22/repo/http_sources.list.ali /etc/apt/sources.list

RUN apt update -y 
RUN apt install -y tzdata ca-certificates
RUN apt install -y wget curl git vim tar bzip2 unzip tree rsync htop zsh
RUN apt install -y passwd sudo man-db tig 
RUN apt install -y gcc g++ make automake cmake 
RUN apt install -y openssh-client psmisc sysstat strace lsof hostname 
RUN apt install -y iproute2 net-tools telnet ncat tcpdump ethtool 
RUN apt install -y iptables ipset iputils-ping
RUN apt install -y python2.7 python3-pip
RUN apt install -y mysql-client redis 

# 时区
ENV TZ "Asia/Shanghai"
# 禁用交互式提示
ENV DEBIAN_FRONTEND noninteractive
# terminal colors with xterm
ENV TERM xterm
ENV HOME /root

#------------------------------------------------------------
# golang

ARG GO_VER=go1.25.1.linux-amd64
COPY pkgs/go/${GO_VER}.tar.gz /tmp/go/
RUN echo "Install golang ..." \
    && tar -zxf /tmp/go/${GO_VER}.tar.gz -C /usr/local \
    && rm -rf /tmp/go/
ENV PATH="$PATH:/usr/local/go/bin:${HOME}/go/bin"
RUN go env -w GOPROXY=https://goproxy.cn,direct \
    && go env -w GO111MODULE=on \
    && go env -w GOSUMDB='off'

#------------------------------------------------------------
# pip2
COPY pkgs/pip2 /tmp/pip2
RUN echo "Install pip2 ..." \
    && cd /tmp/pip2; python2.7 get-pip.py --no-index --find-links=packages \
    && rm -rf /tmp/pip2/

#------------------------------------------------------------
# config
COPY configs/home /tmp/configs/
RUN echo "Install config ..." \
    && cp /tmp/configs/.inputrc ${HOME}/.inputrc \
    && cp /tmp/configs/.gitconfig ${HOME}/.gitconfig \
    && mkdir -p ${HOME}/.pip \
    && cp /tmp/configs/pip.conf ${HOME}/.pip/pip.conf \
    && rm -rf /tmp/configs/

#------------------------------------------------------------
# fzf and bat
ARG FZF_VER=fzf-0.67.0
COPY pkgs/fzf/* /tmp/fzf/
RUN echo "Install fzf ..." \
	&& tar -xzf /tmp/fzf/${FZF_VER}-linux_amd64.tar.gz -C /usr/local/bin \
	&& cd /tmp/fzf && tar -xzf /tmp/fzf/${FZF_VER}.tar.gz \
	&& mv /tmp/fzf/${FZF_VER} ${HOME}/.fzf \
	&& ${HOME}/.fzf/install \
	&& rm -rf /tmp/fzf

ARG BAT_VER=bat-v0.26.0-x86_64-unknown-linux-musl
COPY pkgs/bat/* /tmp/bat/
RUN echo "Install bat ..." \
	&& cd /tmp/bat && tar -xzf /tmp/bat/${BAT_VER}.tar.gz \
	&& cp /tmp/bat/${BAT_VER}/bat /usr/local/bin \
	&& rm -rf /tmp/bat

WORKDIR ${HOME}

CMD ["/bin/bash"]
