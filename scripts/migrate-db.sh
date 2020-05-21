#!/bin/bash

set -x
set -e

python manager.py db migrate
python manager.py db upgrade
