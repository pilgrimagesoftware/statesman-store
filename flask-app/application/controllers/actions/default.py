__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
default.py
- Set default item value action
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


def execute(team_id:str, user_id:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, args: %s", team_id, user_id, args)

    if len(args) < 1:
        blocks = build_error_blocks('Usage: `default <name> <value>`.')
        return blocks, True

    # get current state collection
    user = create_or_fetch_user(user_id, team_id)
    collection = get_current_collection(user)
    if collection is None:
        blocks = build_error_blocks('Unable to set item default; no current collection is set.\nTry one of these:') + list_collections(user_id, team_id)
        return blocks, True

    name = args[0].lower()
    if len(args) == 1:
        # value is None, user wants to remove it
        value = None
    else:
        value = " ".join(args[1:])
    item = StateItem.query.filter_by(collection_id=collection.id, name=name).one_or_none()
    if item is None:
        blocks = build_error_blocks(f'No item exists for name *{name}*.')
    else:
        if not check_item_permission(user, item, model_constants.PERMISSION_WRITE):
            blocks = build_error_blocks('Unable to set default on this item; you do not have permission to write to it.')
            return blocks, True

        item.default_value = value

        db.session.add(item)
        db.session.commit()

        blocks = build_message_blocks(f'Updated item *{name}* with default value *{value}*.')

    return blocks, False


def help_info():
    return ('default',
            'Set Default',
            'Set a item\'s default value: `default <name> <value>`',
            None)
