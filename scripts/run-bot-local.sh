#!/bin/bash

set -x
set -e
set -o pipefail

cd flask-app

pipenv install -r requirements.txt

pipenv run $(pwd)/python appserver.py
