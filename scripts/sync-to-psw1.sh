#!/bin/bash

set -x
set -e

rsync -av \
    --exclude=.git/ \
    --exclude=.gitignore \
    --exclude=.vscode/ \
    --exclude=.env \
    --exclude=.pgenv \
    --exclude=.redisenv \
    --exclude=venv/ \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    ./ \
    psw1:/opt/statesman/flask-app

ssh psw1 "chown -R statesman:statesman /opt/statesman"
