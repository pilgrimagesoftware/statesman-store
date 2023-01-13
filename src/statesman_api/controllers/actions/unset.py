__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
unset.py
- Unset state item action
"""


from flask import current_app
from statesman_api.db import db
from statesman_api.models.state_collection import StateCollection
from statesman_api.models.state_item import StateItem
from statesman_api.utils import build_message_data, build_error_data
from statesman_api.utils.user import set_current_collection, create_or_fetch_user, get_current_collection
from statesman_api.utils.collection import list_collections
from statesman_api.utils.access import check_collection_permission, check_item_permission
from statesman_api.models import constants as model_constants
import logging


def execute(org_id: str, user_id: str, args: list) -> list:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) != 1:
        data = build_error_data("Usage: `unset <name>`.")
        return data

    # get current state collection
    user = create_or_fetch_user(user_id, org_id)
    collection = get_current_collection(user)
    if collection is None:
        data = build_error_data("Unable to uset item; no current collection is set.\nTry one of these:") + list_collections(user_id, org_id)
        return data

    name = args[0]
    item = StateItem.query.filter_by(collection_id=collection.id, name=name).one_or_none()
    if item is not None:
        if not check_item_permission(user, item, model_constants.PERMISSION_WRITE):
            data = build_error_data("Unable to unset this item; you do not have permission to write to it.")
            return data

        db.session.delete(item)
        db.session.commit()

        data = build_message_data(f"Removed item *{name}*.")

    return data, True


def help_info():
    return ("unset", "Unset", "Remove an item: `unset <name>`", None)
