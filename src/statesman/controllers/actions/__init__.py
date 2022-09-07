__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""


from flask import current_app
import importlib


class ValidationException(Exception):
    pass


def validate_action(params:list):
    current_app.logger.debug("params: %s", params)

    if len(params) == 0:
        raise ValidationException('Incorrect number of parameters')

    command = params[0]
    action_spec = importlib.util.find_spec(f'application.controllers.actions.{command}')
    if action_spec is None:
        raise ValidationException(f'Unknown command: {command}')

    return command, params[1:]


def execute_action(team_id:str, user_id:str, command:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, command: %s, args: %s", team_id, user_id, command, args)

    module = importlib.import_module(f'application.controllers.actions.{command}')
    current_app.logger.debug("module: %s", module)
    func = getattr(module, 'execute')
    current_app.logger.debug("func: %s", func)
    blocks = func(team_id, user_id, args)
    current_app.logger.debug("blocks: %s", blocks)

    return blocks
