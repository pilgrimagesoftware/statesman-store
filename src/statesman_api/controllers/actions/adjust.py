__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
adjust.py
- Adjust an item's value
"""


from flask import current_app
from statesman_api.db import db
from statesman_api.models.state_collection import StateCollection
from statesman_api.models.state_item import StateItem
from statesman_api.utils import build_response, build_error_response, add_response_items
from statesman_api.utils.user import set_current_collection, create_or_fetch_user, get_current_collection
from statesman_api.utils.collection import list_collections
from statesman_api.utils.access import check_collection_permission, check_item_permission
from statesman_api.models import constants as model_constants
from statesman_api.utils.item import adjust_item
from statesman_api.utils.args import parse_args
import logging


def execute(org_id: str, user_id: str, args: list) -> dict:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) != 3:
        return build_error_response("Usage: `adj[ust] <name> <+|-|*|/> <value>`.")

    # get current state collection
    user = create_or_fetch_user(user_id, org_id)
    collection = get_current_collection(user)
    if collection is None:
        data = build_error_response("Unable to adjust item's value; no current collection is set.")
        data = add_response_items(data, list_collections(user_id, org_id))
        return data

    parsed_args = parse_args(args)
    name = parsed_args["name"]
    op = parsed_args["op"]
    value = parsed_args["value"]
    item = StateItem.query.filter_by(collection_id=collection.id, name=name).one_or_none()
    if item is None:
        data = build_error_response(f"No item exists for name *{name}*.")
    else:
        if not check_item_permission(user, item, model_constants.PERMISSION_WRITE):
            return build_error_response("Unable to adjust item; you do not have permission to write to it.")

        if op == "+":
            op = model_constants.ADJUST_OP_ADD
        elif op == "-":
            op = model_constants.ADJUST_OP_SUBTRACT
        elif op == "*":
            op = model_constants.ADJUST_OP_MULTIPLY
        elif op == "/":
            op = model_constants.ADJUST_OP_DIVIDE
        else:
            return build_error_response(f"Unable to adjust item; unknown or unsupported operator: {op}")

        try:
            adjust_item(item, op, value)
        except:
            return build_error_response("Unable to adjust item; it's value is not an number.")

        db.session.add(item)
        db.session.commit()

        data = build_response(f"Adjusted item *{name}*'s value by *{value}*: {item.value}.")

    return data


def help_info():
    return ("adjust", "Adjust", "Adjust an item's value: `adj[ust] <name> <+|-|*|/><value>`", None)
