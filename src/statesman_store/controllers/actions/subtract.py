__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
subtract.py
- Decrement an item's value
"""


from flask import current_app
from statesman_store.db import db
from statesman_store.models.state_collection import StateCollection
from statesman_store.models.state_item import StateItem
from statesman_store.utils import build_response, build_error_response, add_response_data
from statesman_store.utils.user import set_current_collection, create_or_fetch_user, get_current_collection
from statesman_store.utils.collection import list_collections
from statesman_store.utils.access import check_collection_permission, check_item_permission
from statesman_store.models import constants as model_constants
from statesman_store.utils.item import adjust_item
from statesman_store.utils.args import parse_args
import logging


def execute(org_id: str, user_id: str, args: list) -> dict:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) != 2:
        return build_error_response("Usage: `add|inc[rement] <name> <value>`.")

    # get current state collection
    user = create_or_fetch_user(user_id, org_id)
    collection = get_current_collection(user)
    if collection is None:
        data = build_response(
            messages=["Unable to increment item's value; no current collection is set.\nTry one of these:"],
            collection_list=list_collections(user_id, org_id),
        )
        return data

    parsed_args = parse_args(args)
    name = parsed_args["name"]
    value = parsed_args["value"]
    item = StateItem.query.filter_by(collection_id=collection.id, name=name).one_or_none()
    if item is None:
        return build_error_response(f"No item exists for name *{name}*.")

    if not check_item_permission(user, item, model_constants.PERMISSION_WRITE):
        return build_error_response("Unable to adjust item; you do not have permission to write to it.")

    try:
        adjust_item(item, model_constants.ADJUST_OP_ADD, value)
    except:
        data = build_error_response("Unable to adjust item; it's value is not an number.")
        return {"data": data, "private": True}

    db.session.add(item)
    db.session.commit()

    data = build_response(messages=[f"Updated item *{name}*'s value by *{value}*: {item.value}."])

    return data


def help_info():
    return ("add", "Add", "Add to an item's value: `add|inc[rement] <name> <value>`", None)
