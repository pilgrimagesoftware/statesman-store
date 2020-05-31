__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
item.py
- Item utilities
"""


from flask import current_app
import json
import os
from application import constants
from application.common.exceptions import SignatureException, ActionNotSupportedException
from application.models.state_collection import StateCollection
from application.models.state_item import StateItem
from application.models.user import User
from application.models import constants as model_constants
from application.db import db
from application.utils.user import create_or_fetch_user
from application.utils.access import check_collection_permission, check_item_permission
from application import constants


def adjust_item(item:StateItem, op:str, value:str):
    current_app.logger.debug("item: %s, op: %s, value: %s", item, op, value)

    try:
        item_value = float(item.value)

        if op == model_constants.ADJUST_OP_ADD:
            item_value += float(value)
        elif op == model_constants.ADJUST_OP_SUBTRACT:
            item_value -= float(value)
        elif op == model_constants.ADJUST_OP_MULTIPLY:
            item_value *= float(value)
        elif op == model_constants.ADJUST_OP_DIVIDE:
            item_value /= float(value)

        if item_value.is_integer():
            item.value = int(item_value)
        else:
            item.value = item_value

    except ValueError:
        item_values = str(item.value).split(sep=constants.ITEM_SEPARATOR)

        if op == model_constants.ADJUST_OP_ADD:
            item_values.append(value)
        elif op == model_constants.ADJUST_OP_SUBTRACT:
            item_values.remove(value)
        elif op == model_constants.ADJUST_OP_MULTIPLY:
            raise ActionNotSupportedException('Cannot multiply a string.')
        elif op == model_constants.ADJUST_OP_DIVIDE:
            raise ActionNotSupportedException('Connot divide a string.')

        item.value = constants.ITEM_SEPARATOR.join(item_values)

    except Exception as e:
        current_app.logger.exception("Exception trying to adjust item: %s", e)
        raise e
