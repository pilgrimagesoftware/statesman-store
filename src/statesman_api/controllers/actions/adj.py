__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
adj.py
- Synonym for 'adjust'
"""


from flask import current_app
from statesman_api.controllers.actions import adjust


def execute(team_id:str, user_id:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, args: %s", team_id, user_id, args)

    return adjust.execute(team_id, user_id, args)
