#!/bin/bash

mkdir -p /fileserver/data/
python3 -m http.server 8800 --directory /fileserver/data/

