#!/bin/bash

docker run -d \
    --name postgres-statesman \
    -e POSTGRES_PASSWORD=statesman \
    -e POSTGRES_USER=statesman \
    -e POSTGRES_DB=statesman \
    postgres:10

docker run -d \
    --name redis-statesman \
    redis:4
