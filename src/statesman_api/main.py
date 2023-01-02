__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
main.py
- creates a Flask app instance and registers the database object
"""


from flask import Flask, session
from flask_session import Session
# from flask_cors import CORS
# from application.cache import cache
from statesman_api import constants
from logging.config import dictConfig
from statesman_api.blueprints import error_page
# from application.controllers.minecraft import load_servers
from werkzeug.exceptions import HTTPException
from redis.client import Redis
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware
from flask_executor import Executor


def create_app(app_name=constants.APPLICATION_NAME):
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s %(module)s, line %(lineno)d: %(message)s',
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
    app.config.from_object("statesman_api.config.BaseConfig")
    # env = DotEnv(app)
    # cache.init_app(app)

    session = Session(app)

    # cors = CORS(app, resources={r"/*": {"origins": "*"}})

    wsgi = SentryWsgiMiddleware(app)

    app.executor = Executor(app)

    # from application.blueprints.main.home import blueprint as home_blueprint
    # app.register_blueprint(home_blueprint, url_prefix="/")

    from statesman_api.blueprints.api import blueprint as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    # from application.blueprints.apps import blueprint as apps_blueprint
    # app.register_blueprint(apps_blueprint, url_prefix="/apps")

    # from application.blueprints.account import blueprint as account_blueprint
    # app.register_blueprint(account_blueprint, url_prefix="/account")

    # from application.blueprints.auth import blueprint as auth_blueprint
    # app.register_blueprint(auth_blueprint, url_prefix="/auth")

    # from application.blueprints.main.health import blueprint as health_blueprint
    # app.register_blueprint(health_blueprint, url_prefix="/health")

    # from application.blueprints.billing import blueprint as billing_blueprint
    # app.register_blueprint(billing_blueprint, url_prefix="/billing")

    from statesman_api.blueprints.health import blueprint as health_blueprint
    app.register_blueprint(health_blueprint, url_prefix="/health")

    from statesman_api.db import db
    # from flask_migrate import Migrate
    db.init_app(app)
    # migrate = Migrate(app, db)

    # vue = Vue(app)

    # app.wsgi_app = SassMiddleware(app.wsgi_app, {
    #     'application': ('static/sass', 'static/css', '/static/css')
    # })
    # scss = Scss(app, static_dir='static', asset_dir='assets')

    # load_servers(app)

    print(app.url_map)

    # app.debug = True

    return app
