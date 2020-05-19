#!/bin/bash

set -x
set -e
set -o pipefail

sudo docker run \
    -d \
    --name manager \
    --hostname manager \
    -v $(pwd):/app \
    -v /opt/minecraft/scripts:/scripts \
    -v /opt/minecraft/servers:/servers \
    -v /opt/minecraft/supervisor:/opt/minecraft/supervisor \
    --net host \
    --workdir /app \
    --restart unless-stopped \
    python:3.8 \
    /app/run.sh
