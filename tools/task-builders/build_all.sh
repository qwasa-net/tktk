#!/bin/bash

SCRIPT_SRC="${BASH_SOURCE[0]}"
SCRIPT_SRC_DIR="$( cd "$( dirname "${SCRIPT_SRC}" )" >/dev/null 2>&1 && pwd )"
PYTHON="${SCRIPT_SRC_DIR}/../../.env/bin/python"
CPWD=`pwd`

# call generators
cd "${SCRIPT_SRC_DIR}"
find "${SCRIPT_SRC_DIR}" -type d | while read dirname
do
    echo "${dirname}"
    cd "${dirname}"
    for g in tasks-generator-*.py
    do
        "${PYTHON}" "${g}"
    done
done

# load
cd "${SCRIPT_SRC_DIR}"
export PYTHONPATH=.:"${SCRIPT_SRC_DIR}/../../pw"
export DJANGO_SETTINGS_MODULE="pw.settings"
"${PYTHON}" "${SCRIPT_SRC_DIR}/load_games.py" */*-games.json "$@"

# done
cd "${CPWD}"