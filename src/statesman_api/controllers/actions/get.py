__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
get.py
- Get current state action
"""


from flask import current_app
import redis
from statesman_api.db import db
from statesman_api.models.state_collection import StateCollection
from statesman_api.utils import build_response, build_error_response, add_response_items, add_response_message
from statesman_api.utils.user import create_or_fetch_user, get_current_collection
from statesman_api.utils.collection import list_collections, get_collection_items
from statesman_api.utils.item import get_item
from statesman_api.utils.args import parse_args
import logging


def execute(org_id: str, user_id: str, args: list) -> dict:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) != 0:
        return build_error_response("Usage: `get [<item>]`.")

    user = create_or_fetch_user(user_id, org_id)

    parsed_args = parse_args(args)
    item_name = parsed_args["item"]

    collection = get_current_collection(user)
    if collection is None:
        data = build_response("A current collection is not set for you; try one of these.", with_emoji=False)
        data = add_response_message(data, "divider", "type")
        data = add_response_items(data, list_collections(user_id, org_id))
        return data

    data = build_response("The current collection:")
    data = add_response_items(data, [{"collection": collection.name, "creator": collection.creator_id}])

    if item_name:
        item = get_item(item_name)
        if item:
            data = add_response_items(data, [item])
        else:
            return build_error_response(f"No item found named '{item_name}'.")
    else:
        data = add_response_items(data, get_collection_items(collection, user))

    return data


def help_info():
    return ("get", "Get", "Get the current state.", "Get")
