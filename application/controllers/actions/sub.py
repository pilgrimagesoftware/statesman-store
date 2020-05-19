__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
sub.py
- Alias for 'subtract'
"""


from flask import current_app
from application.models import constants as model_constants
from application.controllers.actions import adjust
from application.utils.args import check_args


def execute(team_id:str, user_id:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, args: %s", team_id, user_id, args)

    # allows for a missing value, assumed to be 1
    updated_args = check_args(args, model_constants.OPERATOR_SYMBOL_SUBTRACT, 1)
    return adjust.execute(team_id, user_id, updated_args)
