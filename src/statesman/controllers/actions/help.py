__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
help.py
- State collection help action
"""


from flask import current_app
import redis
import importlib
from application.utils import get_package_modules


def execute(team_id:str, user_id:str, args:list) -> list:
    current_app.logger.debug("team_id: %s, user_id: %s, args: %s", team_id, user_id, args)

    modules = get_package_modules('application.controllers.actions')
    current_app.logger.debug("modules: %s", modules)

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "You can use the following commands to interact with Statesman, the state-tracking bot:"
            }
        },
        {
            "type": "divider"
        },
    ]
    for module_name in modules:
        current_app.logger.debug("module_name: %s", module_name)
        try:
            module = importlib.import_module(module_name)
            func = getattr(module, 'help_info')
            help_cmd, help_title, help_desc, help_button = func()
            current_app.logger.debug("cmd: %s, title: %s, desc: %s, button: %s", help_cmd, help_title, help_desc, help_button)

            action = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"`{help_cmd}`: *{help_title}*\n{help_desc}"
                },
            }
            if help_button is not None:
                action['accessory'] = {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": help_button,
                    },
                    "value": help_cmd,
                }

            blocks.append(action)
        except:
            current_app.logger.debug("Module %s didn't have help information, skipping it.", module_name)

    current_app.logger.debug("blocks: %s", blocks)

    return blocks, True
