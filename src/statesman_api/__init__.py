__author__ = "Paul Schifferer <paul@schifferers.net>"
__version__ = "1.0.75"
"""
"""

import sentry_sdk
import os, logging
from statesman_api import constants
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from dotenv import load_dotenv, find_dotenv


ENV_FILE = find_dotenv()
logging.info("ENV_FILE: %s", ENV_FILE)
if ENV_FILE:
    logging.info("Loading .env file...")
    load_dotenv(ENV_FILE)


logging.info("Initializing Sentry...")
sentry_sdk.init(
    dsn=os.environ[constants.SENTRY_DSN],
    environment=os.environ.get(constants.SENTRY_ENV) or "Development",
    integrations=[
        FlaskIntegration(),
    ],
    traces_sample_rate=1.0,
    _experiments={
        "profiles_sample_rate": 1.0,
    },
)
