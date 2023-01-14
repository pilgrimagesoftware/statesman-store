__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
use.py
- State use action
"""


from flask import current_app
import redis
from statesman_api.db import db
from statesman_api.models.state_collection import StateCollection
from statesman_api.utils import build_response, build_error_response
from statesman_api.utils.user import set_current_collection, create_or_fetch_user
from statesman_api.utils.args import parse_args
import logging


def execute(org_id: str, user_id: str, args: list) -> dict:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    if len(args) != 1:
        return build_error_response("Usage: `use <name>`.")

    # check to see if collection already exists (for team)
    parsed_args = parse_args(args)
    name = parsed_args["name"]
    collection = StateCollection.query.filter_by(org_id=org_id, name=name).first()
    if collection is None:
        return build_error_response("A collection with that name does not exist.")

    user = create_or_fetch_user(user_id, org_id)
    if set_current_collection(name, user) is None:
        return build_error_response("You do not have permission to read the specified collection.")

    data = build_response(f"Your current collection has been set to *{name}*.")

    return data


def help_info():
    return ("use", "Use", "Set a collection as the current one: `use <name>`", None)
