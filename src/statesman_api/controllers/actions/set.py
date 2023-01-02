__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
set.py
- Set state item action
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


def execute(team_id:str, user_id:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, args: %s", team_id, user_id, args)

    if len(args) < 2:
        blocks = build_error_blocks('Unable to set item; usage: `set <name> <value> [default=<default>] [label=<label>] [permission=<default-permission>]`.')
        return blocks

    # get current state collection
    user = create_or_fetch_user(user_id, team_id)
    collection = get_current_collection(user)
    if collection is None:
        blocks = build_error_blocks('Unable to set item; no current collection is set.\nTry one of these:') + list_collections(user_id, team_id)
        return blocks

    name = args[0]
    value = args[1]
    item = StateItem.query.filter_by(collection_id=collection.id, name=name).one_or_none()
    if item is None:
        if not check_collection_permission(user, collection, model_constants.PERMISSION_WRITE):
            blocks = build_error_blocks('Unable to create this item; you do not have permission to change this collection.')
            return blocks

        item = StateItem(collection, user_id, team_id, name, value)

        blocks = build_message_blocks(f'Created new item *{name}* with value *{value}*.')
    else:
        if not check_item_permission(user, item, model_constants.PERMISSION_WRITE):
            blocks = build_error_blocks('Unable to update this item; you do not have permission to write to it.')
            return blocks

        item.value = value

        blocks = build_message_blocks(f'Updated item *{name}* with value *{value}*.')

    # handle additional params
    if len(args) > 2:
        current_app.logger.debug("Processing additional parameters to set command: %s", args[2:])

        for other in args[2:]:
            current_app.logger.debug("other: %s", other)
            k,v = other.split(sep='=', maxsplit=2)

            if k == 'default':
                item.default_value = v
            elif k == 'label':
                item.label = v
            elif k == 'permission':
                # TODO
                pass
            else:
                current_app.logger.warning("Unknown extra parameter item: %s", k)

    db.session.add(item)
    db.session.commit()

    return blocks, False


def help_info():
    return ('set',
            'Set',
            'Set a item\'s value: `set <name> <value> [default=<default>] [label=<label>] [permission=<default-permission>]`',
            None)
