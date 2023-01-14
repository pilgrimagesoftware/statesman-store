__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
"""


from flask import current_app
import importlib
import logging


class ValidationException(Exception):
    pass


def validate_action(params:list):
    logging.debug("params: %s", params)

    if len(params) == 0:
        raise ValidationException('Incorrect number of parameters')

    command = params[0]
    action_spec = importlib.util.find_spec(f'statesman_api.controllers.actions.{command}')
    if action_spec is None:
        raise ValidationException(f'Unknown command: {command}')

    return command, params[1:]


def execute_action(org_id:str, user_id:str, command:str, args:list) -> dict:
    logging.debug("org_id: %s, user_id: %s, command: %s, args: %s", org_id, user_id, command, args)

    module = importlib.import_module(f'statesman_api.controllers.actions.{command}')
    logging.debug("module: %s", module)
    func = getattr(module, 'execute')
    logging.debug("func: %s", func)
    data = func(org_id, user_id, args)
    logging.debug("data: %s", data)

    return data.update('command', command)
