__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
set.py
- Set state item action
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
from statesman_store.utils.args import parse_args
import logging


def execute(org_id: str, user_id: str, args: list) -> dict:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) < 2:
        return build_error_response(
            "Unable to set item; usage: `set <name> <value> [default=<default>] [label=<label>] [permission=<default-permission>]`."
        )

    # get current state collection
    user = create_or_fetch_user(user_id, org_id)
    collection = get_current_collection(user)
    if collection is None:
        data = build_response(messages=["Unable to set item; no current collection is set."], collection_list=list_collections(user_id, org_id))
        return data

    parsed_args = parse_args(args)
    name = parsed_args["item"]
    value = parsed_args["value"]
    item = StateItem.query.filter_by(collection_id=collection.id, name=name).one_or_none()
    if item is None:
        if not check_collection_permission(user, collection, model_constants.PERMISSION_WRITE):
            data = build_error_response("Unable to create this item; you do not have permission to change this collection.")
            return data

        item = StateItem(collection, user_id, org_id, name, value)
        logging.debug("item: %s", item)

        data = build_response(messages=[f"Created new item *{name}* with value *{value}*."])
    else:
        if not check_item_permission(user, item, model_constants.PERMISSION_WRITE):
            data = build_error_response("Unable to update this item; you do not have permission to write to it.")
            return data

        item.value = value
        logging.debug("item: %s", item)

        data = build_response(messages=[f"Updated item *{name}* with value *{value}*."])

    logging.debug("data: %s", data)

    # handle additional params
    if len(args) > 2:
        logging.debug("Processing additional parameters to set command: %s", args[2:])

        for other in args[2:]:
            logging.debug("other: %s", other)
            k, v = other.split(sep="=", maxsplit=2)

            if k == "default":
                item.default_value = v
            elif k == "label":
                item.label = v
            elif k == "permission":
                # TODO
                pass
            else:
                logging.warning("Unknown extra parameter item: %s", k)

    db.session.add(item)
    db.session.commit()

    logging.debug("data: %s", data)
    return data


def help_info():
    return ("set", "Set", "Set a item's value: `set <name> <value> [default=<default>] [label=<label>] [permission=<default-permission>]`", None)
