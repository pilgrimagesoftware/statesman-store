__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
access.py
- Access utilities
"""


from flask import current_app
import json
import os
from statesman import constants
from statesman.common.exceptions import SignatureException
from statesman.models.state_collection import StateCollection, StateCollectionUserPermission
from statesman.models.state_item import StateItem, StateItemUserPermission
from statesman.models.user import User
from statesman.models import constants as model_constants
from statesman.db import db


def check_collection_permission(user:User, collection:StateCollection, permission:str) -> bool:
    current_app.logger.debug("user: %s, collection: %s, permission: %s", user, collection, permission)

    perm = StateCollectionUserPermission.query.filter_by(user_id=user.id, collection_id=collection.id).one_or_none()
    current_app.logger.debug("perm: %s", perm)

    # no permission object implicitly grants permission
    if perm is None:
        current_app.logger.debug("No permission is set for user %s; allowing.", user)
        return True

    # is the user blocked?
    if perm.permission == model_constants.PERMISSION_BLOCKED:
        current_app.logger.debug("Permission for user is set to 'blocked'; disallowing.")
        return False

    # check for write permission
    if permission == model_constants.PERMISSION_WRITE and perm.permission == model_constants.PERMISSION_WRITE:
        current_app.logger.debug("Permission request is to write and user is granted; allowing.")
        return True

    # check for read
    if permission == model_constants.PERMISSION_READ:
        current_app.logger.debug("Permission request is to read; allowing.")
        return True

    current_app.logger.debug("Fell through permission check; disallowing.")
    return False


def check_item_permission(user:User, item:StateItem, permission:str) -> bool:
    current_app.logger.debug("user: %s, item: %s, permission: %s", user, item, permission)

    perm = StateItemUserPermission.query.filter_by(user_id=user.id, item_id=item.id).one_or_none()
    current_app.logger.debug("perm: %s", perm)

    # no permission object implicitly grants permission
    if perm is None:
        current_app.logger.debug("No permission is set for user %s; allowing.", user)
        return True

    # is the user blocked?
    if perm.permission == model_constants.PERMISSION_BLOCKED:
        current_app.logger.debug("Permission for user is set to 'blocked'; disallowing.")
        return False

    # check for write permission
    if permission == model_constants.PERMISSION_WRITE and perm.permission == model_constants.PERMISSION_WRITE:
        current_app.logger.debug("Permission request is to write and user is granted; allowing.")
        return True

    # check for read
    if permission == model_constants.PERMISSION_READ:
        current_app.logger.debug("Permission request is to read; allowing.")
        return True

    current_app.logger.debug("Fell through permission check; disallowing.")
    return False


def update_collection_permission(user:User, collection:StateCollection, permission:str):
    current_app.logger.debug("user: %s, collection: %s, permission: %s", user, collection, permission)

    perm = StateCollectionUserPermission.query.filter_by(user_id=user.id, collection_id=collection.id).one_or_none()
    current_app.logger.debug("perm: %s", perm)

    if perm:
        current_app.logger.info("Updating existing permission %s with value %s", perm, permission)
        perm.permission = permission
    else:
        current_app.logger.info("Creating new permission ('%s') for user %s on collection %s.", permission, user, collection)
        perm = StateCollectionUserPermission(user.id, collection.id, permission)

    db.session.add(perm)
    db.session.commit()


def update_item_permission(user:User, item:StateItem, permission:str):
    current_app.logger.debug("user: %s, item: %s, permission: %s", user, item, permission)

    perm = StateCollectionUserPermission.query.filter_by(user_id=user.id, collection_id=collection.id).one_or_none()
    current_app.logger.debug("perm: %s", perm)

    if perm:
        current_app.logger.info("Updating existing permission %s with value %s", perm, permission)
        perm.permission = permission
    else:
        current_app.logger.info("Creating new permission ('%s') for user %s on item %s.", permission, user, item)
        perm = StateItemUserPermission(user.id, item.id, permission)

    db.session.add(perm)
    db.session.commit()


def remove_collection_permission(user:User, collection:StateCollection):
    current_app.logger.debug("user: %s, collection: %s", user, collection)

    perm = StateCollectionUserPermission.query.filter_by(user_id=user.id, collection_id=collection.id).one_or_none()
    current_app.logger.debug("perm: %s", perm)

    if perm:
        current_app.logger.debug("Removing existing permission for user %s on collection %s", user, collection)
        db.session.delete(perm)
        db.session.commit()


def remove_item_permission(user:User, item:StateItem):
    current_app.logger.debug("user: %s, item: %s", user, item)

    perm = StateCollectionUserPermission.query.filter_by(user_id=user.id, item_id=item.id).one_or_none()
    current_app.logger.debug("perm: %s", perm)

    if perm:
        current_app.logger.debug("Removing existing permission for user %s on item %s", user, item)
        db.session.delete(perm)
        db.session.commit()
