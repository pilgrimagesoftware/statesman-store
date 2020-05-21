#!/bin/bash

docker run -d \
    --name pg-statesman \
    --env-file .pgenv \
    --restart=unless-stopped \
    postgres:10

docker run -d \
    --name redis-statesman \
    --env-file .redisenv \
    --restart=unless-stopped \
    redis:4
