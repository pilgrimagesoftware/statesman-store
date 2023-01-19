__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
main.py
- creates a Flask app instance and registers the database object
"""


from flask import Flask, session
from flask_session import Session

# from application.cache import cache
from statesman_store import constants
from logging.config import dictConfig
from statesman_store.blueprints import error_page
from werkzeug.exceptions import HTTPException
from redis.client import Redis
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware
from flask_executor import Executor
import os


def create_app(app_name=constants.APPLICATION_NAME):
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s %(pathname)s %(funcName)s, line %(lineno)d: %(message)s",
                }
            },
            "handlers": {"wsgi": {"class": "logging.StreamHandler", "stream": "ext://flask.logging.wsgi_errors_stream", "formatter": "default"}},
            "root": {"level": os.environ.get(constants.LOG_LEVEL, "INFO"), "handlers": ["wsgi"]},
        }
    )

    app = Flask(app_name)
    app.config.from_object("statesman_store.config.BaseConfig")
    # env = DotEnv(app)
    # cache.init_app(app)

    app.session = Session(app)

    app.sentry = SentryWsgiMiddleware(app)

    app.executor = Executor(app)

    from statesman_store.blueprints.api.state import blueprint as state_blueprint

    app.register_blueprint(state_blueprint)

    from statesman_store.blueprints.health import blueprint as health_blueprint, register_health_check_service_hook
    from statesman_store.messaging.healthcheck import health_check as messaging_health_check
    from statesman_store.db.healthcheck import health_check as db_health_check

    register_health_check_service_hook("messaging", messaging_health_check)
    register_health_check_service_hook("db", db_health_check)
    app.register_blueprint(health_blueprint)

    from statesman_store.db import db
    from flask_migrate import Migrate

    db.init_app(app)
    migrate = Migrate(app, db)

    # from statesman_store.messaging import amqp_run
    # app.executor.submit(amqp_run)
    from statesman_store.messaging.consumer import consumer_thread

    app.consumer_thread = consumer_thread

    print(app.url_map)

    return app
