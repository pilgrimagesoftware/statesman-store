__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
item.py
- Item utilities
"""


from flask import current_app
import json
import os
from statesman import constants
from statesman.common.exceptions import SignatureException
from statesman.models.state_collection import StateCollection
from statesman.models.state_item import StateItem
from statesman.models.user import User
from statesman.models import constants as model_constants
from statesman.db import db
from statesman.utils.user import create_or_fetch_user
from statesman.utils.access import check_collection_permission, check_item_permission


def adjust_item(item:StateItem, op:str, value:str):
    current_app.logger.debug("item: %s, op: %s, value: %s", item, op, value)

    if op == model_constants.ADJUST_OP_ADD:
        item.value += value
    elif op == model_constants.ADJUST_OP_SUBTRACT:
        item.value -= value
    elif op == model_constants.ADJUST_OP_MULTIPLY:
        item.value *= value
    elif op == model_constants.ADJUST_OP_DIVIDE:
        item.value /= value
