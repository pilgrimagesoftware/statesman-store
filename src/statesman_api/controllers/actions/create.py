__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
create.py
- State creation action
"""


from flask import current_app
from statesman_api.db import db
from statesman_api.models.state_collection import StateCollection
from statesman_api.utils import build_message_data, build_error_data
from statesman_api.utils.user import create_or_fetch_user, set_current_collection
from statesman_api.utils.args import parse_args
import logging


def execute(org_id: str, user_id: str, args: list) -> list:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) == 0:
        data = build_error_data("Usage: `create <name>`.")
        return data, True

    # check to see if collection already exists (for team)
    parsed_args = parse_args(args)
    name = parsed_args["name"]
    collection = StateCollection.query.filter_by(org_id=org_id, name=name).one_or_none()
    if collection is not None:
        data = build_error_data("A collection with that name already exists.")
        return data, True

    user = create_or_fetch_user(user_id, org_id)

    # create collection
    collection = StateCollection(user, name)

    db.session.add(collection)
    db.session.commit()

    set_current_collection(name, user)

    data = build_message_data(f"Your collection, *{name}*, has been created.")

    return data, True


def help_info():
    return ("create", "Create", "Create a new collection: `create <name>`", None)
