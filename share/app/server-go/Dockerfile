FROM local.registry.io:9000/devel/ubuntu-22.04-local:latest

COPY go.mod go.sum /tmp/mod/
RUN set -eux; \
    cd /tmp/mod \
    && go mod download

RUN go install github.com/swaggo/swag/cmd/swag@latest

WORKDIR /wine/debox/share/app/server-go

CMD [ "/bin/bash" ]
