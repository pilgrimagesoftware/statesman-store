__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
user.py
- User utilities
"""


from flask import current_app
import json, logging
import os
from statesman_store import constants
from statesman_store.common.exceptions import SignatureException
from statesman_store.models.state_collection import StateCollection, StateCollectionUserPermission
from statesman_store.models.state_item import StateItem, StateItemUserPermission
from statesman_store.models.user import User
from statesman_store.models import constants as model_constants
from statesman_store.db import db
from statesman_store.utils.access import check_collection_permission, check_item_permission


def create_or_fetch_user(user_id: str, org_id: str) -> User:
    logging.debug("user_id: %s, org_id: %s", user_id, org_id)

    user = User.query.filter_by(user_id=user_id).one_or_none()
    if user is None:
        user = User(org_id, user_id)

        db.session.add(user)
        db.session.commit()

    return user


def get_current_collection(user: User) -> StateCollection:
    logging.debug("user: %s", user)

    collection_id = user.current_state_id
    collection = StateCollection.query.filter_by(id=collection_id).one_or_none()

    if collection is None:
        logging.info("User %s does not have a current collection set.", user)
        return None

    if not check_collection_permission(user, collection, model_constants.PERMISSION_READ):
        logging.info("User %s is not permitted to read collection %s", user, collection)
        return None

    return collection


def set_current_collection(name: str, user: User) -> StateCollection:
    logging.debug("name: %s, user: %s", name, user)

    collection = StateCollection.query.filter_by(name=name, org_id=user.org_id).one_or_none()
    if collection is None:
        logging.warning("Can't set current collection for user %s; collection not found: %s", user.id, name)
        return

    if not check_collection_permission(user, collection, model_constants.PERMISSION_READ):
        logging.info("User %s is not permitted to read collection %s", user, collection)
        return None

    user.current_state_id = collection.id

    db.session.add(user)
    db.session.commit()

    return collection
