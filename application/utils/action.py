__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
access.py
- Access utilities
"""


from flask import current_app


def get_action_value(action:dict) -> str:
    current_app.logger.debug("action: %s", action)

    action_type = action.get('type')
    current_app.logger.debug("action_type: %s", action_type)

    if action_type == 'button':
        current_app.logger.debug("Handling button action.")
        value = action.get('value')
    elif action_type == 'overflow':
        current_app.logger.debug("Handling overflow action.")
        value = action.get('selected_action', {}).get('value')
    else:
        current_app.logger.warning("Unknown action type: %s", action_type)
        value = None

    current_app.logger.debug("Returning value: %s", value)
    return value
