#!/bin/sh

EMAIL=xxx@xx.com
NAME=note
ADDR=http://192.168.2.71
SERVER_ID=B7CJ-NEVH-CEPL-BNSB


java -jar atlassian-agent.jar \
	-d -m ${EMAIL} -n ${NAME} \
	-p conf -o ${ADDR} \
	-s ${SERVER_ID}

