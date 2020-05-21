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
from application.models.state_collection import StateCollection
from application.models.state_item import StateItem
from application.models.user import User
from application.models import constants as model_constants
from application.db import db
from application.utils.user import create_or_fetch_user
from application.utils.access import check_collection_permission, check_item_permission


def get_collection_items(collection:StateCollection, user:User) -> list:
    current_app.logger.debug("collection: %s, user: %s", collection, user)

    items = StateItem.query.filter_by(collection_id=collection.id).order_by(StateItem.name).all()
    if len(items) == 0:
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"_Collection *{collection.name}* is empty_."
                }
            },
        ]
        return blocks

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Collection: *<sc://{collection.name}/{collection.id}|{collection.name}>*"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Use"
                },
                "value": f"use {collection.name}"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"_Items_:"
            }
        },
    ]

    # fields = []
    for item in items:
        if not check_item_permission(user, item, model_constants.PERMISSION_READ):
            current_app.logger.debug("User %s does not have permission to read item %s.", user, item)
            continue

        label = item.name
        if item.label is not None and len(item.label) > 0:
            label = f"{item.label} (`{item.name}`)"

        item_info = f"{label}: *{item.value}*"

        if ((collection.creator_id == user.user_id or item.creator_id == user.user_id)
            and
            (item.default_value is not None and len(item.default_value) > 0)):
            item_info += f"\n_Default value_: *{item.default_value}*"

        field = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": item_info,
            },
            "accessory": {
                "type": "overflow",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "+1"
                        },
                        "value": f"add {item.name}"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "+5"
                        },
                        "value": f"add {item.name} 5"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "-1"
                        },
                        "value": f"subtract {item.name}"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "-5"
                        },
                        "value": f"subtract {item.name} 5"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Unset"
                        },
                        "value": f"unset {item.name}"
                    },
                ]
            },
        }
        blocks.append(field)

        # blocks.append({
        #     "type": "actions",
        #     "elements": [
        #         {
        #             "text": {
        #                 "type": "plain_text",
        #                 "emoji": True,
        #                 "text": "+1"
        #             },
        #             "style": "primary",
        #             "value": f"add {item.name}"
        #         },
        #         {
        #             "text": {
        #                 "type": "plain_text",
        #                 "emoji": True,
        #                 "text": "+5"
        #             },
        #             "style": "primary",
        #             "value": f"add {item.name} 5"
        #         },
        #         {
        #             "text": {
        #                 "type": "plain_text",
        #                 "emoji": True,
        #                 "text": "-1"
        #             },
        #             "value": f"subtract {item.name}"
        #         },
        #         {
        #             "text": {
        #                 "type": "plain_text",
        #                 "emoji": True,
        #                 "text": "-5"
        #             },
        #             "value": f"subtract {item.name} 5"
        #         },
        #         {
        #             "text": {
        #                 "type": "plain_text",
        #                 "emoji": True,
        #                 "text": "Unset"
        #             },
        #             "style": "danger",
        #             "value": f"unset {item.name}"
        #         },
        #     ]
        # })

    # blocks.append({
    #     "type": "section",
    #     "fields": fields,
    # })

    return blocks


def list_collections(user_id:str, team_id:str) -> list:
    current_app.logger.debug("user_id: %s, team_id: %s", user_id, team_id)

    user = create_or_fetch_user(user_id, team_id)
    collections = StateCollection.query.filter_by(team_id=team_id).all()

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "_Here are the state collections you can use_:"
            }
        },
        {
            "type": "divider"
        },
    ]

    for c in collections:
        if not check_collection_permission(user, c, model_constants.PERMISSION_READ):
            current_app.logger.debug("User %s does not have permission to read collection %s.", user, c)
            continue

        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{c.name}*\nCreated by <@{c.creator_id}>"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "Use"
                },
                "value": f"use {c.name}"
            }
        })

    return blocks
