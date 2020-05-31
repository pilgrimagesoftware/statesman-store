__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
main.py
- creates a Flask app instance and registers the database object
"""


from flask import Flask, session
from flask_session import Session
from application import constants
from logging.config import dictConfig
from application.blueprints import error_page
from werkzeug.exceptions import HTTPException
from redis.client import Redis
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware


def create_app(app_name=constants.APPLICATION_NAME):
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s %(pathname)s, line %(lineno)d: %(message)s',
            }
        },
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    app = Flask(app_name)
    app.config.from_object("application.config.BaseConfig")

    session = Session(app)

    wsgi = SentryWsgiMiddleware(app)

    from application.blueprints.api import blueprint as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    from application.db import db
    # from flask_migrate import Migrate
    db.init_app(app)
    # migrate = Migrate(app, db)

    # print(app.url_map)



    return app
