__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
state_item.py
- StateItem model object
"""

from datetime import datetime
from statesman_store.db import db
from sqlalchemy.dialects.postgresql import ENUM
from statesman_store.models import constants as model_constants


class User(db.Model):
    """
    An object that represents a user.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String(50), nullable=False)
    org_id = db.Column(db.String(30), nullable=False)
    current_state_id = db.Column(db.Integer, db.ForeignKey("state_collections.id"))

    def __init__(self, org_id: str, user_id: str):
        self.org_id = org_id
        self.user_id = user_id

    def to_dict(self):
        return dict(
            id=self.id,
            org_id=self.org_id,
            user_id=self.user_id,
            current_state_id=self.current_state_id,
            creator_id=self.creator_id,
            created_at=self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            updated_at=self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        )
