__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
create.py
- State creation action
"""


from flask import current_app
from statesman_store.db import db
from statesman_store.models.state_collection import StateCollection
from statesman_store.utils import build_response, build_error_response
from statesman_store.utils.user import create_or_fetch_user, set_current_collection
from statesman_store.utils.args import parse_args
import logging


def execute(org_id: str, user_id: str, args: list) -> dict:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) == 0:
        return build_error_response("Usage: `create <name>`.")

    # check to see if collection already exists (for team)
    parsed_args = parse_args(args)
    name = parsed_args["name"]
    collection = StateCollection.query.filter_by(org_id=org_id, name=name).one_or_none()
    if collection is not None:
        return build_error_response("A collection with that name already exists.")

    user = create_or_fetch_user(user_id, org_id)

    # create collection
    collection = StateCollection(user, name)

    db.session.add(collection)
    db.session.commit()

    set_current_collection(name, user)

    data = build_response(messages=[f"Your collection, *{name}*, has been created."], private=True)

    return data


def help_info():
    return ("create", "Create", "Create a new collection: `create <name>`", None)
