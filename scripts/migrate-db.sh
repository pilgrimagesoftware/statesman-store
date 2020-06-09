#!/bin/bash

set -x
set -e

cd flask-app

python manager.py db migrate
python manager.py db upgrade
