__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
adj.py
- Synonym for 'adjust'
"""


from flask import current_app
from statesman_store.controllers.actions import adjust
import logging


def execute(org_id:str, user_id:str, args:list) -> dict:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    return adjust.execute(org_id, user_id, args)
