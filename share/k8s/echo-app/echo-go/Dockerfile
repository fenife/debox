FROM golang:1.22.5-alpine3.20 as builder

RUN go env -w GOPROXY='https://goproxy.cn,direct' \
    && go env -w GO111MODULE='on' \
    && go env -w GOSUMDB='off'

WORKDIR /go/src/app

COPY go.mod go.sum ./
RUN go mod download 

COPY *.go .
RUN GOOS=linux GOARCH=amd64 go build -o echo-app ./


FROM alpine-base:3.20
COPY --from=builder /go/src/app/echo-app /go/src/app/
EXPOSE 6000
ENTRYPOINT ["/go/src/app/echo-app"]


