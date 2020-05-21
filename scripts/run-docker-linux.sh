#!/bin/bash

set -x
set -e
set -o pipefail

# sudo docker network create statesman
sudo docker run \
    -d \
    --name statesman \
    --hostname statesman \
    -v $(pwd):/app \
    --workdir /app \
    -p 8899:8899 \
    --link pg-statesman \
    --link redis-statesman \
    --restart unless-stopped \
    python:3.8 \
    /app/run.sh
