__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
unset.py
- Unset state item action
"""


from flask import current_app
from statesman_api.db import db
from statesman_api.models.state_collection import StateCollection
from statesman_api.models.state_item import StateItem
from statesman_api.utils import build_response, build_error_response, add_response_data, add_response_message
from statesman_api.utils.user import set_current_collection, create_or_fetch_user, get_current_collection
from statesman_api.utils.collection import list_collections
from statesman_api.utils.access import check_collection_permission, check_item_permission
from statesman_api.models import constants as model_constants
from statesman_api.utils.args import parse_args
import logging


def execute(org_id: str, user_id: str, args: list) -> dict:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) != 1:
        return build_error_response("Usage: `unset <name>`.")

    # get current state collection
    user = create_or_fetch_user(user_id, org_id)
    collection = get_current_collection(user)
    if collection is None:
        data = build_response(
            messages=["Unable to uset item; no current collection is set."],
            success=False,
            collection_list=list_collections(user_id, org_id),
            private=True,
        )
        return data

    parsed_args = parse_args(args)
    name = parsed_args["name"]
    item = StateItem.query.filter_by(collection_id=collection.id, name=name).one_or_none()
    if item is None:
        return build_error_response(f"Item {name} not found.")

    if not check_item_permission(user, item, model_constants.PERMISSION_WRITE):
        return build_error_response("Unable to unset this item; you do not have permission to write to it.")

    db.session.delete(item)
    db.session.commit()

    # data = build_response(f"Removed item *{name}*.")
    data = build_response(messages=[f"Item {name} has been removed."], private=True)
    return data


def help_info():
    return ("unset", "Unset", "Remove an item: `unset <name>`", None)
