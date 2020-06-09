#!/bin/bash

set -x
set -e
set -o pipefail

scriptdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null && pwd)"

pushd $scriptdir > /dev/null 2>&1

apt update
apt install -y supervisor

# python -m pip install --upgrade pip
pip install -r requirements.txt

python appserver.py

popd > /dev/null 2>&1
