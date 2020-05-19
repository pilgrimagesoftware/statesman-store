__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
create.py
- State creation action
"""


from flask import current_app
from application.db import db
from application.models.state_collection import StateCollection
from application.utils import build_message_blocks, build_error_blocks
from application.utils.user import create_or_fetch_user, set_current_collection


def execute(team_id:str, user_id:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, args: %s", team_id, user_id, args)

    if len(args) == 0:
        blocks = build_error_blocks('Usage: `create <name>`.')
        return blocks

    # check to see if collection already exists (for team)
    name = args[0]
    collection = StateCollection.query.filter_by(team_id=team_id, name=name).one_or_none()
    if collection is not None:
        blocks = build_error_blocks('A collection with that name already exists.')
        return blocks

    user = create_or_fetch_user(user_id, team_id)

    # create collection
    collection = StateCollection(user, name)

    db.session.add(collection)
    db.session.commit()

    set_current_collection(name, user)

    blocks = build_message_blocks(f'Your collection, *{name}*, has been created.')

    return blocks, True


def help_info():
    return ('create',
            'Create',
            'Create a new collection: `create <name>`',
            None)
