__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
state_item.py
- StateItem model object
"""

from datetime import datetime
from statesman_api.db import db
from sqlalchemy.dialects.postgresql import ENUM
from statesman_api.models import constants as model_constants
from statesman_api.models.state_collection import StateCollection


class StateItem(db.Model):
    """
    An object that represents a state item to track.
    """
    __tablename__ = 'state_items'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    collection_id = db.Column(db.Integer, db.ForeignKey('state_collections.id'))
    org_id = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(100), nullable=True)
    default_value = db.Column(db.String(100), nullable=True)
    label = db.Column(db.String(50), nullable=True)

    def __init__(self, collection:StateCollection, creator_id:str, org_id:str, name:str, value:str):
        self.collection_id = collection.id
        self.creator_id = creator_id
        self.org_id = org_id
        self.name = name
        self.value = value

    def to_dict(self):
        return dict(id=self.id,
                    org_id=self.org_id,
                    name=self.name,
                    value=self.value,
                    default_value=self.default_value,
                    label=self.label,
                    collection_id=self.collection_id,
                    creator_id=self.creator_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.updated_at.strftime('%Y-%m-%d %H:%M:%S'))


class StateItemUserPermission(db.Model):
    """
    An object that represents a user permission for a state item
    """
    __tablename__ = 'item_permissions'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('state_items.id'))
    permission = db.Column(db.String(10), default=model_constants.PERMISSION_READ)

    def __init__(self, user_id:str, item:StateItem, permission:str = model_constants.PERMISSION_READ):
        self.user_id = user_id
        self.item_id = item.id
        self.permission = permission

    def to_dict(self):
        return dict(id=self.id,
                    user_id=self.user_id,
                    item_id=self.item_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'))
