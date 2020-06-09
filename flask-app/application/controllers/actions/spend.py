__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
spend.py
- Spend an item's value into another item
"""


from flask import current_app
from application.db import db
from application.models.state_collection import StateCollection
from application.models.state_item import StateItem
from application.utils import build_message_blocks, build_error_blocks
from application.utils.user import set_current_collection, create_or_fetch_user, get_current_collection
from application.utils.collection import list_collections
from application.utils.access import check_collection_permission, check_item_permission
from application.models import constants as model_constants
from application.utils.item import adjust_item


def execute(team_id:str, user_id:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, args: %s", team_id, user_id, args)

    if len(args) < 2:
        blocks = build_error_blocks('Usage: `spend <source-name> <dest-name> [<value>]`.')
        return blocks, True

    # get current state collection
    user = create_or_fetch_user(user_id, team_id)
    collection = get_current_collection(user)
    if collection is None:
        blocks = build_error_blocks('Unable to spend item; no current collection is set.\nTry one of these:') + list_collections(user_id, team_id)
        return blocks, True

    source_name = args[0].lower()
    dest_name = args[1].lower()
    if len(args) > 2:
        quantity = int(args[2])
    else:
        quantity = 1

    source_item = StateItem.query.filter_by(collection_id=collection.id, name=source_name).one_or_none()
    if source_item is None:
        blocks = build_error_blocks(f'No item exists for name *{source_name}*.')
        return blocks, True
    if not check_item_permission(user, source_item, model_constants.PERMISSION_WRITE):
        blocks = build_error_blocks('Unable to spend from item; you do not have permission to write to it.')
        return blocks, True

    try:
        adjust_item(source_item, model_constants.ADJUST_OP_SUBTRACT, quantity)
    except:
        blocks = build_error_blocks(f'Unable to adjust item *{source_name}*; its value is not a number.')
        return blocks, True

    dest_item = StateItem.query.filter_by(collection_id=collection.id, name=dest_name).one_or_none()
    if dest_item is None:
        dest_item = StateItem(collection, user_id, team_id, dest_name, quantity)
    else:
        try:
            adjust_item(dest_item, model_constants.ADJUST_OP_ADD, quantity)
        except:
            blocks = build_error_blocks(f'Unable to adjust item *{dest_name}*; its value is not a number.')
            return blocks, True

    db.session.add(source_item)
    db.session.add(dest_item)
    db.session.commit()

    blocks = build_message_blocks(f'Spent item *{source_name}* into *{dest_name}*: {quantity}.')

    return blocks, False


def help_info():
    return ('spend',
            'Spend',
            'Spend an item\'s value into another item: `spend <source-name> <dest-name> [<value>]`',
            None)
