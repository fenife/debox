#!/bin/bash

# start supervisor
/usr/bin/supervisord -n >> /dev/null 2>&1 &

