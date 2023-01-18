__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
collection.py
- Collection utilities
"""


import json
import os, logging
from statesman_store import constants
from statesman_store.common.exceptions import SignatureException
from statesman_store.models.state_collection import StateCollection
from statesman_store.models.state_item import StateItem
from statesman_store.models.user import User
from statesman_store.models import constants as model_constants
from statesman_store.db import db
from statesman_store.utils.user import create_or_fetch_user
from statesman_store.utils.access import check_collection_permission, check_item_permission


def get_collection_items(collection: StateCollection, user: User) -> list[dict]:
    logging.debug("collection: %s, user: %s", collection, user)

    items = StateItem.query.filter_by(collection_id=collection.id).all()
    logging.debug("items: %s", items)
    if len(items) == 0:
        return []

    data = []
    # {"text": f"Collection: *<{collection.name}|{collection.name}>*"},
    # {"type": "divider"},
    # {"text": f"_Items_:"},

    for item in items:
        logging.debug("item: %s", item)
        if not check_item_permission(user, item, model_constants.PERMISSION_READ):
            logging.debug("User %s does not have permission to read item %s.", user, item)
            continue

        item_info = {"value": item.value, "name": item.name}

        if item.label is not None and len(item.label) > 0:
            item_info["label"] = item.label

        if item.default_value is not None and len(item.default_value) > 0:
            item_info["default"] = item.default_value

        logging.debug("item_info: %s", item_info)
        data.append({"item": item_info})

    logging.debug("data: %s", data)
    return data


def list_collections(user_id: str, org_id: str) -> list[dict]:
    logging.debug("user_id: %s, org_id: %s", user_id, org_id)

    user = create_or_fetch_user(user_id, org_id)
    collections = StateCollection.query.filter_by(org_id=org_id).all()

    data = [
        # {"text": "Here are the collections you can use:"}, {"type": "divider"}
    ]

    for c in collections:
        if not check_collection_permission(user, c, model_constants.PERMISSION_READ):
            logging.debug("User %s does not have permission to read collection %s.", user, c)
            continue

        data.append({"collection": c.name, "creator": c.creator_id})

    return data
