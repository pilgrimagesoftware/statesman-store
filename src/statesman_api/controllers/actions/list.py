__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
list.py
- State collection list action
"""


from flask import current_app
import redis
from statesman_api.models.state_collection import StateCollection
from statesman_api.utils import build_response, build_error_response, add_response_data
from statesman_api.utils.collection import list_collections
import logging


def execute(org_id: str, user_id: str, args: list) -> dict:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) != 0:
        return build_error_response("Usage: `list`.")

    count = StateCollection.query.filter_by(org_id=org_id).count()

    if count == 0:
        build_response(messages=["_There are no collections that you can access._"], success=False, private=True)

    data = build_response(title="Your collections", private=True, collection_list=list_collections(user_id, org_id))

    return data


def help_info():
    return ("list", "List", "List collections that are available.", "List")
