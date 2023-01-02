__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
subtract.py
- Decrement an item's value
"""


from flask import current_app
from statesman_api.db import db
from statesman_api.models.state_collection import StateCollection
from statesman_api.models.state_item import StateItem
from statesman_api.utils import build_message_blocks, build_error_blocks
from statesman_api.utils.user import set_current_collection, create_or_fetch_user, get_current_collection
from statesman_api.utils.collection import list_collections
from statesman_api.utils.access import check_collection_permission, check_item_permission
from statesman_api.models import constants as model_constants
from statesman_api.utils.item import adjust_item


def execute(team_id:str, user_id:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, args: %s", team_id, user_id, args)

    if len(args) != 2:
        blocks = build_error_blocks('Usage: `add|inc[rement] <name> <value>`.')
        return blocks

    # get current state collection
    user = create_or_fetch_user(user_id, team_id)
    collection = get_current_collection(user)
    if collection is None:
        blocks = build_error_blocks('Unable to increment item\'s value; no current collection is set.\nTry one of these:') + list_collections(user_id, team_id)
        return blocks

    name = args[0]
    value = args[1]
    item = StateItem.query.filter_by(collection_id=collection.id, name=name).one_or_none()
    if item is None:
        blocks = build_error_blocks(f'No item exists for name *{name}*.')
    else:
        if not check_item_permission(user, item, model_constants.PERMISSION_WRITE):
            blocks = build_error_blocks('Unable to adjust item; you do not have permission to write to it.')
            return blocks

        try:
            adjust_item(item, model_constants.ADJUST_OP_ADD, value)
        except:
            blocks = build_error_blocks('Unable to adjust item; it\'s value is not an number.')
            return blocks

        db.session.add(item)
        db.session.commit()

        blocks = build_message_blocks(f'Updated item *{name}*\'s value by *{value}*: {item.value}.')

    return blocks, False


def help_info():
    return ('add',
            'Add',
            'Add to an item\'s value: `add|inc[rement] <name> <value>`',
            None)
