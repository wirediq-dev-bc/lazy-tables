#!/bin/bash

READ_MY_LINK="$(readlink -f $0)"
WHEREAMI="${READ_MY_LINK%/*}"
PROGNAME="${READ_MY_LINK##*/}"

sh_c='sh -c'
ECHO=${ECHO:-}
[ "$ECHO" ] && sh_c='echo'
SETX=${SETX:-}
[ "$SETX" ] && set -x

VOLUME_NAME='persist-xlsx'
IMAGE_NAME='lazy-tables'
CONTAINER_NAME='uci-tables'
XLSX_DIR='/usr/src/app/docs/xlsx'

TOP_LEVEL=${WHEREAMI}/../..
SAVE_DIR="${TOP_LEVEL}/dmount"
CUR_DIR="$PWD"
MODE=


Usage () {
    cat >&2 <<- EOF
usage: $PROGNAME

Options:
 -b, --build        Build lazy-tables Docker image.
 -r, --run          Run lazy-tables Docker image.
 -c, --copy         Copy .xlsx files from named volume to host.
 -v, --view         View contents of ${XLSX_DIR} directory.
 -h, --help         Print this help message and exit.

EOF
exit 1
}

Error () {
    echo -e "-${PROGNAME%.*} error: $1\n$2" > /dev/stderr
    exit 1
}

parse_args () {
    case "$1" in
        -b | --build ) MODE='build';;
        -r | --run ) MODE='run';;
        -v | --view ) MODE='view';;
        -c | --copy ) MODE='copy';;
        -h | --help ) Usage;;
        * ) Error "Unknown CLI token: ${1}";;
    esac
}

cleanup () {
    # Remove old named volumes
    docker volume ls | grep -q "$VOLUME_NAME" && docker volume rm "$VOLUME_NAME"
    # Remove old image builds
    docker image ls | grep -q "$IMAGE_NAME" && docker image rm "$IMAGE_NAME"
    # Remove transient containers
    docker ps -a | grep -q "$CONTAINER_NAME" && docker rm "$CONTAINER_NAME"
}

image_builder () {
    cd "$TOP_LEVEL"
    docker volume create "$VOLUME_NAME"
    docker build -t "$IMAGE_NAME" .
}

run_lazy_tables () {
    docker run -it --rm --volume "$VOLUME_NAME":/usr/src --name "$CONTAINER_NAME" "$IMAGE_NAME"
}

view_docs () {
    docker run -it --rm --volume "$VOLUME_NAME":/usr/src alpine ls -la "$XLSX_DIR"
}

copy_docs () {
    if [ ! -d "$SAVE_DIR" ]; then
        mkdir "$SAVE_DIR"
    fi
    docker run -it --rm \
        --volume "$VOLUME_NAME":/usr/src \
        --volume "$SAVE_DIR":/tmp \
        alpine cp -r "$XLSX_DIR" /tmp
}

main () {
    case "$MODE" in
        build ) cleanup; image_builder;;
        run ) run_lazy_tables;;
        view ) view_docs;;
        copy ) copy_docs;;
    esac
}

[ "$1" ] || Usage
parse_args "$1"
main
