__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
adjust.py
- Adjust an item's value
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

    if len(args) != 3:
        blocks = build_error_blocks('Usage: `adj[ust] <name> <+|-|*|/> <value>`.')
        return blocks, True

    # get current state collection
    user = create_or_fetch_user(user_id, team_id)
    collection = get_current_collection(user)
    if collection is None:
        blocks = build_error_blocks('Unable to adjust item\'s value; no current collection is set.\nTry one of these:') + list_collections(user_id, team_id)
        return blocks, True

    name = args[0].lower()
    op = args[1]
    value = args[2]
    item = StateItem.query.filter_by(collection_id=collection.id, name=name).one_or_none()
    if item is None:
        blocks = build_error_blocks(f'No item exists for name *{name}*.')
    else:
        if not check_item_permission(user, item, model_constants.PERMISSION_WRITE):
            blocks = build_error_blocks('Unable to adjust item; you do not have permission to write to it.')
            return blocks, True

        if op == model_constants.OPERATOR_SYMBOL_ADD:
            op = model_constants.ADJUST_OP_ADD
        elif op == model_constants.OPERATOR_SYMBOL_SUBTRACT:
            op = model_constants.ADJUST_OP_SUBTRACT
        elif op == model_constants.OPERATOR_SYMBOL_MULTIPLY:
            op = model_constants.ADJUST_OP_MULTIPLY
        elif op == model_constants.OPERATOR_SYMBOL_DIVIDE:
            op = model_constants.ADJUST_OP_DIVIDE
        else:
            blocks = build_error_blocks(f'Unable to adjust item; unknown or unsupported operator: {op}')
            return blocks, True

        try:
            adjust_item(item, op, value)
        except:
            blocks = build_error_blocks('Unable to adjust item; its value is not a number or a string.')
            return blocks, True

        db.session.add(item)
        db.session.commit()

        blocks = build_message_blocks(f'Adjusted item *{name}*\'s value: {item.value}.')

        blocks.append({
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Show the collection",
                        "emoji": True
                    },
                    "value": "items"
                },
            ]
        })

    return blocks, False


def help_info():
    return ('adjust',
            'Adjust',
            'Adjust an item\'s value: `adj[ust] <name> <+|-|*|/> <value>`. Note that this works for both numbers (adjusting numerically) and strings (creating a comma-separated list of values).',
            None)
