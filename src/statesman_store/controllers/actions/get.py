__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
get.py
- Get current state action
"""


from flask import current_app
import redis
from statesman_store.db import db
from statesman_store.models.state_collection import StateCollection
from statesman_store.utils import build_response, build_error_response, add_response_data
from statesman_store.utils.user import create_or_fetch_user, get_current_collection
from statesman_store.utils.collection import list_collections, get_collection_items
from statesman_store.utils.item import get_item
from statesman_store.utils.args import parse_args
from statesman_store import constants
import logging


def execute(org_id: str, user_id: str, args: list) -> dict:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) > 1:
        return build_error_response("Usage: `get [<item>]`.")

    user = create_or_fetch_user(user_id, org_id)

    parsed_args = parse_args(args)
    item_name = parsed_args.get("item")

    collection = get_current_collection(user)
    if collection is None:
        return build_response(messages=["A current collection is not set for you."], collection_list=list_collections(user_id, org_id), success=False)

    data = build_response(title="The current collection", collection={"collection": collection.name, "creator": collection.creator_id})

    if item_name:
        item = get_item(item_name)
        if item:
            data = add_response_data(data, items=[item])
        else:
            return build_error_response(f"No item found named '{item_name}'.")
    else:
        items = get_collection_items(collection, user)
        if len(items) == 0:
            data = add_response_data(data, messages=["The collection is empty."])
        else:
            data = add_response_data(data, items=items)

    return data


def help_info():
    return ("get", "Get", "Get the current state.", "Get")
