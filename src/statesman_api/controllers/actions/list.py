__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
list.py
- State collection list action
"""


from flask import current_app
import redis
from statesman_api.models.state_collection import StateCollection
from statesman_api.utils import build_error_data
from statesman_api.utils.collection import list_collections
import logging


def execute(org_id: str, user_id: str, args: list) -> list:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) != 0:
        data = build_error_data("Usage: `list`.")
        return data, True

    count = StateCollection.query.filter_by(org_id=org_id).count()

    if count == 0:
        data = [
            {"text": "_There are no collections that you can access._"},
        ]
        return data, True

    return list_collections(user_id, org_id), True


def help_info():
    return ("list", "List", "List collections that are available.", "List")
