
FROM local.registry.io:9000/library/openresty:1.27.1.2-11-jammy 

RUN echo "prepare server dir ..." \
    && mkdir -p /data/logs/server-lua \
    && mkdir -p /data/server-lua

WORKDIR /data/server-lua

CMD [ "/bin/bash" ]
