__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
current.py
- Get current state action
"""


from flask import current_app
import redis
from statesman_api.db import db
from statesman_api.models.state_collection import StateCollection
from statesman_api.utils import build_message_data, build_error_data
from statesman_api.utils.user import create_or_fetch_user, get_current_collection
from statesman_api.utils.collection import list_collections, get_collection_items
import logging


def execute(org_id: str, user_id: str, args: list) -> list:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) != 0:
        data = build_error_data("Usage: `current`.")
        return data

    user = create_or_fetch_user(user_id, org_id)

    collection = get_current_collection(user)
    if collection is None:
        data = build_message_data("A current collection is not set for you; try one of these:") + list_collections(user_id)
        return data

    data = get_collection_items(collection, user)

    return data, False


def help_info():
    return ("current", "Current", "Get the current state.", "Current")
