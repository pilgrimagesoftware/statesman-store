__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
healthcheck.py
- DB health check
"""

import logging, os, time
from statesman_store.db import db
from statesman_store import constants
from statesman_store.models.state_collection import StateCollection, StateCollectionUserPermission
from statesman_store.models.state_item import StateItem, StateItemUserPermission
from statesman_store.models.user import User

last_health_status = {
    "ping": {"status": "Unknown", "checked": None},
    "db": {
        "host": os.environ[constants.DB_HOST],
        "port": os.environ[constants.DB_PORT],
        "user": os.environ[constants.DB_USER],
        "database": os.environ[constants.DB_NAME],
        "options": os.environ.get(constants.DB_OPTS, ""),
    },
    "objects": {},
}


def health_check() -> dict:
    logging.info("Checking health of database...")

    try:
        last_health_status["objects"] = {
            "StateCollection": StateCollection.query.count(),
            "StateCollectionUserPermission": StateCollectionUserPermission.query.count(),
            "StateItem": StateItem.query.count(),
            "StateItemUserPermission": StateItemUserPermission.query.count(),
            "User": User.query.count(),
        }
        last_health_status["ping"]["status"] = "healthy"
    except Exception as e:
        logging.exception("Exception while checking database:", e)
        last_health_status["ping"]["status"] = "error"

    last_health_status["ping"]["checked"] = str(time.time())

    return last_health_status
