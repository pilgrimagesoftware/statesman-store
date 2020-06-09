#!/bin/bash

set -x
set -e
set -o pipefail
unset DOCKER_HOST

cd discord-relay

docker rm discord-relay || echo
docker run \
    -it --rm \
    --name discord-relay \
    --hostname discord-relay \
    -v $(pwd):/app \
    -p 8899:8899 \
    --env-file .env \
    --workdir /app \
    python:3.8 \
    /app/run.sh
