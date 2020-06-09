#!/bin/bash

set -x
set -e

cd flask-app

rm -rf migrations
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
