#!/bin/bash

. ${BASE_OPT_DIR}/include/sh/common.sh

function _mkdir() {
    if [ ! -d "$IMAGE_SAVE_DIR" ]; then
        mkdir -p $IMAGE_SAVE_DIR
    fi
}

function _ls_dir() {
    ls $IMAGE_SAVE_DIR
}

function save() {
    _mkdir
    local _image=$1
    local _name=`echo $_image | cut -d ":" -f 1`
    local _image_tar="$IMAGE_SAVE_DIR/$_name.tar"
    if [ -f $_image_tar ]; then 
        rm $_image_tar 
    fi
    docker save -o $_image_tar $_image
    _ls_dir
}

function load() {
    local _image=$1
    local _name=`echo $_image | cut -d ":" -f 1`
    local _image_tar="$IMAGE_SAVE_DIR/$_name.tar"
    docker load -i $_image_tar
    _ls_dir
}

if [[ -z "$1" ]] || [[ $1 == help ]]; then
    help
else
    set -x
    eval $* 
fi
