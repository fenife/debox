FROM alpine:3.20

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories 
RUN apk -U add bash netcat-openbsd curl \
    && rm -rf /var/cache/apk/*
RUN apk add -U tzdata
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

CMD [ "/bin/bash" ]

