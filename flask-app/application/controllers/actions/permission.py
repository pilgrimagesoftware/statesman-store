__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
permission.py
- Set permissions on a collection or item
"""


from flask import current_app
from application.db import db
from application.models.state_collection import StateCollection, StateCollectionUserPermission
from application.models.state_item import StateItem, StateItemUserPermission
from application.models.user import User
from application.models import constants as model_constants
from application.utils import build_error_blocks, build_message_blocks
from application.utils.access import update_collection_permission, update_item_permission, remove_collection_permission, remove_item_permission

def execute(team_id:str, user_id:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, args: %s", team_id, user_id, args)

    if len(args) != 3:
        blocks = build_error_blocks('Usage: `permission <username> read|write|block|remove collection=<name>|item=<name>`.')
        return blocks, True

    username = args[0]
    op = args[1]
    thing = args[2]

    user = User.query.filter_by(team_id=team_id, username=username).one_or_none()
    if user is None:
        blocks = build_error_blocks(f'Could not find user for: {username}')
        return blocks, True

    if op not in [model_constants.PERMISSION_OP_READ, model_constants.PERMISSION_OP_WRITE,
                  model_constants.PERMISSION_OP_BLOCK, model_constants.PERMISSION_OP_REMOVE]:
        blocks = build_error_blocks(f'Unsupported operation: {op}')
        return blocks, True

    things = thing.split(sep='=', maxsplit=2)
    thing_type = things[0]
    thing_name = things[1]

    if thing_type not in [model_constants.PERMISSION_THING_COLLECTION, model_constants.PERMISSION_THING_ITEM]:
        blocks = build_error_blocks(f'Unknown type: {thing_type}')
        return blocks, True

    if thing_type == model_constants.PERMISSION_THING_COLLECTION:
        collection = StateCollection.query.filter_by(team_id=user.team_id, name=thing_name).one_or_none()
        if collection is None:
            blocks = build_error_blocks(f'Could not find a collection named: {thing_name}')
            return blocks, True

        perm = StateCollectionUserPermission.query.filter_by(user_id=user.user_id, collection_id=collection.id).one_or_none()
        if perm is None and op != model_constants.PERMISSION_OP_REMOVE:
            perm = StateCollectionUserPermission(user.user_id, collection, op)

    elif thing_type == model_constants.PERMISSION_THING_ITEM:
        item = StateItem.query.filter_by(team_id=user.team_id, name=thing_name.lower()).one_or_none()
        if item is None:
            blocks = build_error_blocks(f'Could not find an item named: {thing_name}')
            return blocks, True

        perm = StateItemUserPermission.query.filter_by(user_id=user.user_id, item_id=item.id).one_or_none()
        if perm is None and op != model_constants.PERMISSION_OP_REMOVE:
            perm = StateItemUserPermission(user.user_id, item, op)

    if perm:
        if op == model_constants.PERMISSION_OP_REMOVE:
            db.session.delete(perm)
        else:
            perm.permission = op
            db.session.add(perm)

        db.session.commit()

    blocks = build_message_blocks('Permission edited.')
    return blocks, False


def help_info():
    return ('permission',
            'Permission',
            'Set permissions on a collection or item: `permission <username> read|write|block|remove collection=<name>|item=<name>`',
            None)
