__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
items.py
- Get current state's items
"""


from flask import current_app
import redis
from application.db import db
from application.models.state_collection import StateCollection
from application.utils import build_message_blocks, build_error_blocks
from application.utils.user import create_or_fetch_user, get_current_collection
from application.utils.collection import list_collections, get_collection_items


def execute(team_id:str, user_id:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, args: %s", team_id, user_id, args)

    if len(args) != 0:
        blocks = build_error_blocks('Usage: `items`.')
        return blocks, True

    user = create_or_fetch_user(user_id, team_id)

    collection = get_current_collection(user)
    if collection is None:
        blocks = build_message_blocks('A current collection is not set for you; try one of these:') + list_collections(user_id)
        return blocks, True

    blocks = get_collection_items(collection, user)

    return blocks, False


def help_info():
    return ('items',
            'Items',
            'Get the current state\'s items.',
            'Items')