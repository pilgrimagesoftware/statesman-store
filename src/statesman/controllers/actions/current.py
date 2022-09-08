__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
current.py
- Get current state action
"""


from flask import current_app
import redis
from statesman.db import db
from statesman.models.state_collection import StateCollection
from statesman.utils import build_message_blocks, build_error_blocks
from statesman.utils.user import create_or_fetch_user, get_current_collection
from statesman.utils.collection import list_collections, get_collection_items


def execute(team_id:str, user_id:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, args: %s", team_id, user_id, args)

    if len(args) != 0:
        blocks = build_error_blocks('Usage: `current`.')
        return blocks

    user = create_or_fetch_user(user_id, team_id)

    collection = get_current_collection(user)
    if collection is None:
        blocks = build_message_blocks('A current collection is not set for you; try one of these:') + list_collections(user_id)
        return blocks

    blocks = get_collection_items(collection, user)

    return blocks, False


def help_info():
    return ('current',
            'Current',
            'Get the current state.',
            'Current')
