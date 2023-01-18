__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
item.py
- Item utilities
"""


from flask import current_app
import json, logging
import os
from statesman_store import constants
from statesman_store.common.exceptions import SignatureException
from statesman_store.models.state_collection import StateCollection
from statesman_store.models.state_item import StateItem
from statesman_store.models.user import User
from statesman_store.models import constants as model_constants
from statesman_store.db import db
from statesman_store.utils.user import create_or_fetch_user
from statesman_store.utils.access import check_collection_permission, check_item_permission


def get_item(name: str) -> StateItem:
    logging.debug("name: %s", name)

    return StateItem.query.filter_by(name=name).one_or_none()


def adjust_item(item: StateItem, op: str, value: str):
    logging.debug("item: %s, op: %s, value: %s", item, op, value)

    if op == model_constants.ADJUST_OP_ADD:
        item.value += value
    elif op == model_constants.ADJUST_OP_SUBTRACT:
        item.value -= value
    elif op == model_constants.ADJUST_OP_MULTIPLY:
        item.value *= value
    elif op == model_constants.ADJUST_OP_DIVIDE:
        item.value /= value
