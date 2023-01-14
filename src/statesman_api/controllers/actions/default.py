__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
default.py
- Set default item value action
"""


from flask import current_app
from statesman_api.db import db
from statesman_api.models.state_collection import StateCollection
from statesman_api.models.state_item import StateItem
from statesman_api.utils import build_response, build_error_response, add_response_data
from statesman_api.utils.user import set_current_collection, create_or_fetch_user, get_current_collection
from statesman_api.utils.collection import list_collections
from statesman_api.utils.access import check_collection_permission, check_item_permission
from statesman_api.models import constants as model_constants
from statesman_api.utils.args import parse_args
import logging


def execute(org_id: str, user_id: str, args: list) -> dict:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) != 2:
        return build_error_response("Usage: `default <name> <value>`.")

    # get current state collection
    user = create_or_fetch_user(user_id, org_id)
    collection = get_current_collection(user)
    if collection is None:
        data = build_response(
            title="No collection",
            messages=["Unable to set item default; no current collection is set."],
            success=False,
            collection_list=list_collections(user_id, org_id),
        )
        return data

    parsed_args = parse_args(args)
    name = parsed_args["name"]
    value = parsed_args["value"]
    item = StateItem.query.filter_by(collection_id=collection.id, name=name).one_or_none()
    if item is None:
        return build_error_response(f"No item exists for name *{name}*.")
    else:
        if not check_item_permission(user, item, model_constants.PERMISSION_WRITE):
            return build_error_response("Unable to set default on this item; you do not have permission to write to it.")

        item.default_value = value

        db.session.add(item)
        db.session.commit()

        data = build_response(messages=[f"Updated item *{name}* with default value *{value}*."], private=True)

    return data


def help_info():
    return ("default", "Set Default", "Set a item's default value: `default <name> <value>`", None)
