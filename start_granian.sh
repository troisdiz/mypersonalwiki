#!/usr/bin/env bash

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     GNU_PREFIX="";;
    Darwin*)    GNU_PREFIX="g";;
    *)          GNU_PREFIX="";;
esac

readonly PROGNAME=$(${GNU_PREFIX}basename $0)
readonly PROGDIR=$(${GNU_PREFIX}readlink -m "$(${GNU_PREFIX}dirname $0)")
readonly ARGS=( "$@" )

readonly PAGES_PATH="${ARGS[0]}"

export GITWIKI_PAGES_PATH="${PAGES_PATH}"
echo "Using pages path: ${GITWIKI_PAGES_PATH}"
"${PROGDIR}"/venv/bin/granian --working-dir "${PROGDIR}"/src --workers 3  --interface wsgi gitwiki.granian:app
