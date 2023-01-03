__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
config.py
- settings for the flask application object
"""


import os
import random
import hashlib
import redis
from statesman_api import constants


class BaseConfig(object):
    DEBUG = bool(os.environ.get(constants.DEBUG, True))
    PORT = int(os.environ.get(constants.PORT, "5000"))
    LOG_LEVEL = os.environ.get(constants.LOG_LEVEL, "INFO")
    APP_SHARED_SECRET = os.environ.get(constants.APP_SHARED_SECRET, "")
    # ASSETS_DEBUG = True
    POSTGRES_HOST = os.environ[constants.DB_HOST]
    POSTGRES_PORT = int(os.environ.get(constants.DB_PORT, "5432"))
    POSTGRES_USER = os.environ[constants.DB_USER]
    POSTGRES_PW = os.environ[constants.DB_PW]
    POSTGRES_DB = os.environ[constants.DB_NAME]
    DB_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///minecraft-manager.db'
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # used for encryption and session management
    SECRET_KEY = os.environ.get(constants.SECRET_KEY) or hashlib.sha256(f"{random.random()}").hexdigest()
    CSRF_TOKEN = os.environ.get(constants.CSRF_TOKEN) or hashlib.sha256(f"{random.random()}").hexdigest()
    CACHE_REDIS_HOST = os.environ[constants.REDIS_HOST]
    CACHE_REDIS_PORT = int(os.environ.get(constants.REDIS_PORT, "6379"))
    CACHE_REDIS_PASSWORD = os.environ.get(constants.REDIS_PW)
    CACHE_REDIS_DB = int(os.environ.get(constants.REDIS_DB, "7"))
    SESSION_TYPE = os.environ.get(constants.SESSION_TYPE, "redis")
    SESSION_REDIS = redis.from_url(f"redis://{os.environ[constants.REDIS_HOST]}:6379")
    EXECUTOR_TYPE = "thread"
    EXECUTOR_MAX_WORKERS = 5
    EXECUTOR_PROPAGATE_EXCEPTIONS = True
