#!/bin/bash

set -x
set -e
set -o pipefail

pipenv install -r requirements.txt

pipenv run $(pwd)/python appserver.py
