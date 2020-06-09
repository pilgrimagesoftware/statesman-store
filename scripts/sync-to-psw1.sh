#!/bin/bash

set -x
set -e

rsync -av \
    --exclude=.git/ \
    --exclude=.gitignore \
    --exclude=.vscode/ \
    --exclude=.env \
    --exclude=.pgenv \
    --exclude=.DS_Store \
    --exclude=.redisenv \
    --exclude=venv/ \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    ./ \
    psw1:/opt/statesman/

ssh psw1 "chown -R statesman:statesman /opt/statesman"
ssh psw1 "chmod 400 /opt/statesman/*/.*env"
