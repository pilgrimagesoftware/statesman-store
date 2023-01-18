__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
reset.py
- Action to reset a collection's items to their default value
"""


from flask import current_app
import redis
from statesman_store.db import db
from statesman_store.models.state_collection import StateCollection
from statesman_store.models.state_item import StateItem
from statesman_store.utils import build_response, build_error_response, add_response_data
from statesman_store.utils.user import set_current_collection, get_current_collection, create_or_fetch_user
from statesman_store.utils.collection import list_collections
from statesman_store.models import constants as model_constants
from statesman_store.utils.args import parse_args
import logging


def execute(org_id: str, user_id: str, args: list) -> dict:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) != 0:
        data = build_error_response("Usage: `reset`.")
        return data

    user = create_or_fetch_user(user_id, org_id)
    collection = get_current_collection(user)
    if collection is None:
        data = build_response(messages=["No collection is set for you."], collection_list=list_collections(user_id, org_id))
        return data

    items = StateItem.query.filter_by(collection_id=collection.id).all()
    for item in items:
        if not check_item_permission(user, item, model_constants.PERMISSION_WRITE):
            logging.debug("User %s does not have permission to write item %s.", user, item)
            continue

        logging.info("Setting item %s value to its default: %s", item, item.default_value)
        item.value = item.default_value

        db.session.add(item)

    db.session.commit()

    data = build_response(messages=[f"Collection *{collection.name}* has been reset."])

    return data


def help_info():
    return ("reset", "Reset", "Reset a collection's item values to their defaults.", "Reset")
