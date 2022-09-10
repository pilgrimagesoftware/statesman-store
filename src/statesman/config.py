__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
config.py
- settings for the flask application object
"""


import os
import random
import hashlib
import redis


print(os.environ) # TODO: remove

class BaseConfig(object):
    DEBUG = bool(os.environ.get('DEBUG') or True)
    # ASSETS_DEBUG = True
    POSTGRES_HOST = os.environ["PGHOST"]
    POSTGRES_PORT = os.environ.get("PGPORT", "5432")
    POSTGRES_USER = os.environ["PGUSER"]
    POSTGRES_PW = os.environ["PGPASSWORD"]
    POSTGRES_DB = os.environ["PGDATABASE"]
    DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///minecraft-manager.db'
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # used for encryption and session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or hashlib.sha256(f"{random.random()}").hexdigest()
    CSRF_TOKEN = os.environ.get('CSRF_TOKEN') or hashlib.sha256(f"{random.random()}").hexdigest()
    CACHE_REDIS_HOST = os.environ['REDIS_HOST']
    CACHE_REDIS_PORT = 6379 # int(os.environ.get('REDIS_PORT', "6379"))
    CACHE_REDIS_DB = int(os.environ.get('REDIS_DB') or 7)
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.from_url(f"redis://{os.environ['REDIS_HOST']}:6379")
