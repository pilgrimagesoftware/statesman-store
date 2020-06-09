#!/bin/bash

set -x
set -e
set -o pipefail
unset DOCKER_HOST

cd flask-app

docker rm statesman || echo
docker run \
    -it --rm \
    --name statesman \
    --hostname statesman \
    -v $(pwd):/app \
    -p 8899:8899 \
    --workdir /app \
    --env-file .env \
    --link postgres-statesman \
    --link redis-statesman \
    python:3.8 \
    /app/run.sh
