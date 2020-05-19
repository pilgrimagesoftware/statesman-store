__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
access.py
- Access utilities
"""


from flask import current_app


def check_args(args:list, op:str, default_value:int) -> list:
    current_app.logger.debug("args: %s, op: %s, default_value: %s", args, op, default_value)

    if len(args) < 2:
        updated_args = [args[0], op, 1]
    else:
        updated_args = [args[0], op, args[1]]

    current_app.logger.debug("updated_args: %s", updated_args)

    return updated_args
