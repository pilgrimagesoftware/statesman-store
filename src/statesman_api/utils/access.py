__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
access.py
- Access utilities
"""


from flask import current_app
import json, logging
import os
from statesman_api import constants
from statesman_api.common.exceptions import SignatureException
from statesman_api.models.state_collection import StateCollection, StateCollectionUserPermission
from statesman_api.models.state_item import StateItem, StateItemUserPermission
from statesman_api.models.user import User
from statesman_api.models import constants as model_constants
from statesman_api.db import db


def check_collection_permission(user: User, collection: StateCollection, permission: str) -> bool:
    logging.debug("user: %s, collection: %s, permission: %s", user, collection, permission)

    perm = StateCollectionUserPermission.query.filter_by(user_id=user.id, collection_id=collection.id).one_or_none()
    logging.debug("perm: %s", perm)

    # no permission object implicitly grants permission
    if perm is None:
        logging.debug("No permission is set for user %s; allowing.", user)
        return True

    # is the user blocked?
    if perm.permission == model_constants.PERMISSION_BLOCK:
        logging.debug("Permission for user is set to 'blocked'; disallowing.")
        return False

    # check for write permission
    if permission == model_constants.PERMISSION_WRITE and perm.permission == model_constants.PERMISSION_WRITE:
        logging.debug("Permission request is to write and user is granted; allowing.")
        return True

    # check for read
    if permission == model_constants.PERMISSION_READ:
        logging.debug("Permission request is to read; allowing.")
        return True

    logging.debug("Fell through permission check; disallowing.")
    return False


def check_item_permission(user: User, item: StateItem, permission: str) -> bool:
    logging.debug("user: %s, item: %s, permission: %s", user, item, permission)

    perm = StateItemUserPermission.query.filter_by(user_id=user.id, item_id=item.id).one_or_none()
    logging.debug("perm: %s", perm)

    # no permission object implicitly grants permission
    if perm is None:
        logging.debug("No permission is set for user %s; allowing.", user)
        return True

    # is the user blocked?
    if perm.permission == model_constants.PERMISSION_BLOCK:
        logging.debug("Permission for user is set to 'blocked'; disallowing.")
        return False

    # check for write permission
    if permission == model_constants.PERMISSION_WRITE and perm.permission == model_constants.PERMISSION_WRITE:
        logging.debug("Permission request is to write and user is granted; allowing.")
        return True

    # check for read
    if permission == model_constants.PERMISSION_READ:
        logging.debug("Permission request is to read; allowing.")
        return True

    logging.debug("Fell through permission check; disallowing.")
    return False


def update_collection_permission(user: User, collection: StateCollection, permission: str):
    logging.debug("user: %s, collection: %s, permission: %s", user, collection, permission)

    perm = StateCollectionUserPermission.query.filter_by(user_id=user.id, collection_id=collection.id).one_or_none()
    logging.debug("perm: %s", perm)

    if perm:
        logging.info("Updating existing permission %s with value %s", perm, permission)
        perm.permission = permission
    else:
        logging.info("Creating new permission ('%s') for user %s on collection %s.", permission, user, collection)
        perm = StateCollectionUserPermission(user.id, collection.id, permission)

    db.session.add(perm)
    db.session.commit()


def update_item_permission(user: User, item: StateItem, permission: str):
    logging.debug("user: %s, item: %s, permission: %s", user, item, permission)

    perm = StateCollectionUserPermission.query.filter_by(user_id=user.id, collection_id=collection.id).one_or_none()
    logging.debug("perm: %s", perm)

    if perm:
        logging.info("Updating existing permission %s with value %s", perm, permission)
        perm.permission = permission
    else:
        logging.info("Creating new permission ('%s') for user %s on item %s.", permission, user, item)
        perm = StateItemUserPermission(user.id, item.id, permission)

    db.session.add(perm)
    db.session.commit()


def remove_collection_permission(user: User, collection: StateCollection):
    logging.debug("user: %s, collection: %s", user, collection)

    perm = StateCollectionUserPermission.query.filter_by(user_id=user.id, collection_id=collection.id).one_or_none()
    logging.debug("perm: %s", perm)

    if perm:
        logging.debug("Removing existing permission for user %s on collection %s", user, collection)
        db.session.delete(perm)
        db.session.commit()


def remove_item_permission(user: User, item: StateItem):
    logging.debug("user: %s, item: %s", user, item)

    perm = StateCollectionUserPermission.query.filter_by(user_id=user.id, item_id=item.id).one_or_none()
    logging.debug("perm: %s", perm)

    if perm:
        logging.debug("Removing existing permission for user %s on item %s", user, item)
        db.session.delete(perm)
        db.session.commit()
