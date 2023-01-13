__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
label.py
- Set item label action
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

    if len(args) != 2:
        data = build_error_data("Usage: `label <name> <value>`.")
        return data

    # get current state collection
    user = create_or_fetch_user(user_id, org_id)
    collection = get_current_collection(user)
    if collection is None:
        data = build_error_data("Unable to set item label; no current collection is set.\nTry one of these:") + list_collections(user_id, org_id)
        return data

    name = args[0]
    value = args[1]
    item = StateItem.query.filter_by(collection_id=collection.id, name=name).one_or_none()
    if item is None:
        data = build_error_data(f"No item exists for name *{name}*.")
    else:
        if not check_item_permission(user, item, model_constants.PERMISSION_WRITE):
            data = build_error_data("Unable to set label on this item; you do not have permission to write to it.")
            return data

        item.label = value

        db.session.add(item)
        db.session.commit()

        data = build_message_data(f"Updated item *{name}* with label *{value}*.")

    return data, False


def help_info():
    return ("label", "Set Label", "Set a item's label: `set <name> <value>`", None)
