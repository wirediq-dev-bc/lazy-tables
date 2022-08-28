#!/bin/bash

READ_MY_LINK="$(readlink -f $0)"
WHEREAMI="${READ_MY_LINK%/*}"
PROGNAME="${READ_MY_LINK##*/}"

sh_c='sh -c'
ECHO=${ECHO:-}
[ "$ECHO" ] && sh_c='echo'
SETX=${SETX:-}
[ "$SETX" ] && set -x

TOP_LEVEL=$WHEREAMI/../..

Usage () {
    cat >&2 <<- EOF
usage: $PROGNAME
EOF
}

Error () {
    echo -e "-${PROGNAME%.*} error: $1\n$2" > /dev/stderr
    exit 1
}

main () {
    MAIN_PY=./app/app/main.py
    if [[ $HOSTNAME  =~ 'BeetBox' ]]; then
        cd $TOP_LEVEL
        venvpy run uci-wizard $MAIN_PY
    else
        python3 $MAIN_PY
    fi
}

main
