__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
increment.py
- Synonym for 'add'
"""


from flask import current_app
from statesman_api.models import constants as model_constants
from statesman_api.controllers.actions import adjust
import logging


def execute(org_id:str, user_id:str, args:list) -> list:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    updated_args = [args[0], model_constants.ADJUST_OP_ADD, args[1]]

    return adjust.execute(org_id, user_id, updated_args)