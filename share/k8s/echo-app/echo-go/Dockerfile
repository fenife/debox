# FROM local.registry.io:9000/devel/ubuntu-22.04-base:latest as builder
FROM local.registry.io:9000/library/golang:1.25-alpine3.22 as builder

RUN go env -w GOPROXY='https://goproxy.cn,direct' \
    && go env -w GO111MODULE='on' \
    && go env -w GOSUMDB='off'

WORKDIR /app/echo-app

COPY go.mod go.sum ./
RUN go mod download 

COPY . .
RUN GOOS=linux GOARCH=amd64 go build -o echo-app ./

# FROM local.registry.io:9000/devel/ubuntu-22.04-base:latest
FROM local.registry.io:9000/devel/alpine-3.20-base:latest
COPY --from=builder /app/echo-app /app/
WORKDIR /app
EXPOSE 6000
ENTRYPOINT ["/app/echo-app"]

