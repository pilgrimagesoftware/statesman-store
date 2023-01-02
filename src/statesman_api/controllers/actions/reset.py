__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
reset.py
- Action to reset a collection's items to their default value
"""


from flask import current_app
import redis
from statesman_api.db import db
from statesman_api.models.state_collection import StateCollection
from statesman_api.models.state_item import StateItem
from statesman_api.utils import build_message_blocks, build_error_blocks
from statesman_api.utils.user import set_current_collection, get_current_collection, create_or_fetch_user
from statesman_api.utils.collection import list_collections
from statesman_api.models import constants as model_constants


def execute(team_id:str, user_id:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, args: %s", team_id, user_id, args)

    if len(args) != 0:
        blocks = build_error_blocks('Usage: `reset`.')
        return blocks

    user = create_or_fetch_user(user_id, team_id)
    collection = get_current_collection(user)
    if collection is None:
        blocks = build_error_blocks('No collection is set for you; try one of these:') + list_collections(user_id, team_id)
        return blocks

    items = StateItem.query.filter_by(collection_id=collection.id).all()
    for item in items:
        if not check_item_permission(user, item, model_constants.PERMISSION_WRITE):
            current_app.logger.debug("User %s does not have permission to write item %s.", user, item)
            continue

        current_app.logger.info("Setting item %s value to its default: %s", item, item.default_value)
        item.value = item.default_value

        db.session.add(item)

    db.session.commit()

    blocks = build_message_blocks(f'Collection *{name}* has been reset.')

    return blocks, True


def help_info():
    return ('reset',
            'Reset',
            'Reset a collection\'s item values to their defaults.',
            'Reset')
