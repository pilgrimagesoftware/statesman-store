__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
constants.py
- Contstants for keys and environment variable names
"""

CLIENT_AUTH_TOKEN = "CLIENT_AUTH_TOKEN"

SENTRY_DSN = "SENTRY_DSN"
SENTRY_ENV = "SENTRY_ENV"

APPLICATION_NAME = "statesman"
PROFILE_KEY = "profile"
JWT_PAYLOAD = "jwt_payload"
CURRENT_USER_ID = "current_user_id"

# configuration
APP_SHARED_SECRET = "APP_SHARED_SECRET"
SEGMENT_WRITE_KEY = "SEGMENT_WRITE_KEY"
DEBUG = "DEBUG"
PORT = "PORT"
LOG_LEVEL = "LOG_LEVEL"
DB_HOST = "DB_HOST"
DB_PORT = "DB_PORT"
DB_USER = "DB_USER"
DB_PW = "DB_PW"
DB_NAME = "DB_NAME"
DB_OPTS = "DB_OPTS"
REDIS_HOST = "REDIS_HOST"
REDIS_PORT = "REDIS_PORT"
REDIS_DB = "REDIS_DB"
REDIS_PW = "REDIS_PW"
LOGSTASH_HOST = "LOGSTASH_HOST"
LOGSTASH_DB_PATH = "LOGSTASH_DB_PATH"
LOGSTASH_TRANSPORT = "LOGSTASH_TRANSPORT"
LOGSTASH_PORT = "LOGSTASH_PORT"
SECRET_KEY = "SECRET_KEY"
CSRF_TOKEN = "CSRF_TOKEN"
SESSION_TYPE = "SESSION_TYPE"
BUILD_INFO_PATH = "BUILD_INFO_PATH"
RABBITMQ_HOST = "RABBITMQ_HOST"
RABBITMQ_PORT = "RABBITMQ_PORT"
RABBITMQ_VHOST = "RABBITMQ_VHOST"
RABBITMQ_EXCHANGE = "RABBITMQ_EXCHANGE"
RABBITMQ_USER = "RABBITMQ_USER"
RABBITMQ_PASSWORD = "RABBITMQ_PASSWORD"
RABBITMQ_QUEUE = "RABBITMQ_QUEUE"
NAMESPACE = "NAMESPACE"
POD = "POD"

INTERNAL_AUTH_TYPE = "Private"
