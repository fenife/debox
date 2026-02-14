# see: https://github.com/coder/code-server/blob/main/ci/release-image/Dockerfile

FROM local.registry.io:9000/library/ubuntu:22.04 as dfs
COPY pkgs /tmp/pkgs

FROM local.registry.io:9000/devel/ubuntu-22.04:latest

ARG CODER_PKG=code-server_4.102.0_amd64.deb
COPY pkgs/coder/${CODER_PKG} /tmp/coder/

RUN --mount=from=dfs,src=/tmp/pkgs,dst=/tmp/pkgs \
    echo "Install code-server ..." \
    && dpkg -i /tmp/pkgs/coder/${CODER_PKG}

# RUN echo "Install code-server ..." \
# 	&& dpkg -i /tmp/coder/${CODER_PKG} \
#     && rm -rf /tmp/coder

COPY pkgs/vscode/ext /tmp/ext
RUN echo "Install code extensions ..." \
    && cd /tmp/ext \
    && code-server --install-extension vscodevim.vim-1.32.4.vsix \
    && code-server --install-extension maattdd.gitless-11.7.2.vsix \
    && code-server --install-extension golang.go-0.52.2.vsix

    # && code-server --install-extension ms-python.python-2025.10.0@linux-x64.vsix \
    # && code-server --install-extension ms-python.vscode-pylance-2025.10.2.vsix \
    # && code-server --install-extension ms-python.debugpy-2025.18.0.vsix \


# COPY pkgs/vscode/ext /tmp/ext
# RUN echo "Install code extensions ..." \
#     && cd /tmp/ext \
#     && code-server --install-extension ms-ceintl.vscode-language-pack-zh-hans-1.102.2025071609.vsix \
#     && code-server --install-extension vscodevim.vim-1.32.4.vsix \
#     && code-server --install-extension ms-python.python-2025.10.0@linux-x64.vsix \
#     && code-server --install-extension ms-python.vscode-pylance-2025.10.2.vsix \
#     && code-server --install-extension maattdd.gitless-11.7.2.vsix \
#     && code-server --install-extension golang.go-0.52.2.vsix

# COPY configs/coder/config.yaml ${HOME}/.config/coder-server/
# && code-server --install-extension ms-python.python-2021.12.1559732655.vsix \

# COPY configs/coder /tmp/coder
# RUN echo "Install coder settings ..." \
#     && cp /tmp/coder/config.yaml ${HOME}/.config/code-server/config.yaml \
#     && cp /tmp/coder/settings.json ${HOME}/.local/share/code-server/User/settings.json

COPY pkgs/coder/bin/*.sh ${HOME}/

# RUN if grep -q 1000 /etc/passwd; then \
#         userdel -r "$(id -un 1000)"; \
#     fi \
#     && adduser --gecos '' --disabled-password coder \
#     && echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd

# ARG FIXUID_VER=fixuid-0.6.0-linux-amd64
# COPY pkgs/fixuid/${FIXUID_VER}.tar.gz /tmp/
# RUN echo "Install fixuid ..." \
#     && tar -xzf /tmp/${FIXUID_VER}.tar.gz -C /usr/local/bin \
#     && chown root:root /usr/local/bin/fixuid \
#     && chmod 4755 /usr/local/bin/fixuid \
#     && mkdir -p /etc/fixuid \
#     && printf "user: coder\ngroup: coder\n" > /etc/fixuid/config.yml

# EXPOSE 8080
# This way, if someone sets $DOCKER_USER, docker-exec will still work as
# the uid will remain the same. note: only relevant if -u isn't passed to
# docker-run.
# USER 1000
# ENV USER=coder
# WORKDIR /home/coder

CMD ["/bin/bash"]
