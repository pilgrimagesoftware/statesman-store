__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
increment.py
- Synonym for 'add'
"""


from flask import current_app
from application.models import constants as model_constants
from application.controllers.actions import adjust


def execute(team_id:str, user_id:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, args: %s", team_id, user_id, args)

    updated_args = [args[0], model_constants.OPERATOR_SYMBOL_ADD, args[1]]
    current_app.logger.debug("updated_args: %s", updated_args)

    return adjust.execute(team_id, user_id, updated_args)
