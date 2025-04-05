FROM stg-registry.me:8810/fenife/local-ubuntu-24.04:latest

COPY go.mod go.sum /tmp/mod/
RUN set -eux; \
    cd /tmp/mod \
    && go mod download

RUN go install github.com/swaggo/swag/cmd/swag@latest

WORKDIR /wine/debox/share/app/server-go

CMD [ "/bin/zsh" ]
