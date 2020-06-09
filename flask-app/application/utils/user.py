__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
user.py
- User utilities
"""


from flask import current_app
import json
import os
from application import constants
from application.common.exceptions import SignatureException
from application.models.state_collection import StateCollection, StateCollectionUserPermission
from application.models.state_item import StateItem, StateItemUserPermission
from application.models.user import User
from application.models import constants as model_constants
from application.db import db
from application.utils.access import check_collection_permission, check_item_permission


def create_or_fetch_user(user_id:str, team_id:str) -> User:
    current_app.logger.debug("user_id: %s, team_id: %s", user_id, team_id)

    user = User.query.filter_by(user_id=user_id).one_or_none()
    if user is None:
        user = User(team_id, user_id)

        db.session.add(user)
        db.session.commit()

    return user


def get_current_collection(user:User) -> StateCollection:
    current_app.logger.debug("user: %s", user)

    collection_id = user.current_state_id
    collection = StateCollection.query.filter_by(id=collection_id).one_or_none()

    if not check_collection_permission(user, collection, model_constants.PERMISSION_READ):
        current_app.logger.info("User %s is not permitted to read collection %s", user, collection)
        return None

    return collection


def set_current_collection(name:str, user:User) -> StateCollection:
    current_app.logger.debug("name: %s, user: %s", name, user)

    collection = StateCollection.query.filter_by(name=name, team_id=user.team_id).one_or_none()
    if collection is None:
        current_app.logger.warning("Can't set current collection for user %s; collection not found: %s", user.id, name)
        return

    if not check_collection_permission(user, collection, model_constants.PERMISSION_READ):
        current_app.logger.info("User %s is not permitted to read collection %s", user, collection)
        return None

    user.current_state_id = collection.id

    db.session.add(user)
    db.session.commit()

    return collection
