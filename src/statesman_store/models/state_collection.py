__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
state_collection.py
- StateCollection model object
"""

from datetime import datetime
from statesman_store.db import db
from sqlalchemy.dialects.postgresql import ENUM
from statesman_store.models import constants as model_constants
from statesman_store.models.user import User


class StateCollection(db.Model):
    """
    An object that represents a state collection.
    """
    __tablename__ = 'state_collections'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    org_id = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, user:User, name:str):
        self.creator_id = user.user_id
        self.org_id = user.org_id
        self.name = name

    def to_dict(self):
        return dict(id=self.id,
                    org_id=self.org_id,
                    name=self.name,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'))


class StateCollectionUserPermission(db.Model):
    """
    An object that represents a user permission for a state collection
    """
    __tablename__ = 'collection_permissions'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    collection_id = db.Column(db.Integer, db.ForeignKey('state_collections.id'))
    permission = db.Column(db.String(10), default=model_constants.PERMISSION_READ)

    def __init__(self, user_id:str, collection:StateCollection, permission:str = model_constants.PERMISSION_READ):
        self.user_id = user_id
        self.collection_id = collection.id
        self.permission = permission

    def to_dict(self):
        return dict(id=self.id,
                    user_id=self.user_id,
                    collection_id=self.collection_id,
                    permission=self.permission,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'))
