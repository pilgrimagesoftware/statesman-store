__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
use.py
- State use action
"""


from flask import current_app
import redis
from statesman_api.db import db
from statesman_api.models.state_collection import StateCollection
from statesman_api.utils import build_message_blocks, build_error_blocks
from statesman_api.utils.user import set_current_collection, create_or_fetch_user


def execute(team_id:str, user_id:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, args: %s", team_id, user_id, args)

    if len(args) != 0:
        blocks = build_error_blocks('Usage: `use <name>`.')
        return blocks

    # check to see if collection already exists (for team)
    name = args[0]
    collection = StateCollection.query.filter_by(team_id=team_id, name=name).first()
    if collection is None:
        blocks = build_error_blocks('A collection with that name does not exist.')
        return blocks

    user = create_or_fetch_user(user_id, team_id)
    if set_current_collection(name, user) is None:
        blocks = build_error_blocks('You do not have permission to read the specified collection.')
        return blocks, True

    blocks = build_message_blocks(f'Your current collection has been set to *{name}*.')

    return blocks, True


def help_info():
    return ('use',
            'Use',
            'Set a collection as the current one: `use <name>`',
            None)
