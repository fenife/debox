

SERVER_LUA_DIR=/data/server-lua
SERVER_LUA_LOG_DIR=/data/logs/server-lua
SERVER_LUA_CONF_FILE=${SERVER_LUA_DIR}/ngx_conf/nginx.conf
SERVER_LUA_PID=${SERVER_LUA_LOG_DIR}/nginx.pid

RESTY_DIR=/usr/local/openresty
NGINX_BIN=${RESTY_DIR}/nginx/sbin/nginx

### start:		start lua server
.PHONY: start
start:
	${NGINX_BIN} -c ${SERVER_LUA_CONF_FILE}

### reload:		reload lua server
.PHONY: reload
reload:
	${NGINX_BIN} -c ${SERVER_LUA_CONF_FILE} -s reload

### stop:		stop lua server
.PHONY: stop
stop:
	kill -TERM `cat ${SERVER_LUA_PID}`

### conf:		test config
.PHONY: conf
conf:
	${NGINX_BIN} -c ${SERVER_LUA_CONF_FILE} -t

### c:			test config
.PHONY: c
c: 	conf

### test:		test lua server
ACTION ?= a
.PHONY: test
test:
	curl -i http://127.0.0.1/app/v1/reply?action=${ACTION}
	@echo "\n"

### t:			test lua server
.PHONY: t
t:	test

### log:		tail log
.PHONY: log
log:
	tail -f ${SERVER_LUA_LOG_DIR}/app_error.log -n 30

### help:		show Makefile rules
.PHONY: help
help:
	@echo
	@echo Makefile rules:
	@grep -E '^### [-A-Za-z0-9_]+:' Makefile | sed 's/###/   /'
	@echo

h: help

