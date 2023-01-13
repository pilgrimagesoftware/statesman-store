__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
help.py
- State collection help action
"""


from flask import current_app
import redis
import importlib
from statesman_api.utils import get_package_modules
import logging


def execute(org_id: str, user_id: str, args: list) -> list:
    logging.debug("org_id: %s, user_id: %s, args: %s", org_id, user_id, args)

    modules = get_package_modules("statesman_api.controllers.actions")
    logging.debug("modules: %s", modules)

    data = [
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "You can use the following commands to interact with Statesman, the state-tracking bot:"},
        },
        {"type": "divider"},
    ]
    for module_name in modules:
        logging.debug("module_name: %s", module_name)
        try:
            module = importlib.import_module(module_name)
            func = getattr(module, "help_info")
            help_cmd, help_title, help_desc, help_button = func()
            logging.debug("cmd: %s, title: %s, desc: %s, button: %s", help_cmd, help_title, help_desc, help_button)

            help_info = {
                'command': help_cmd,
                'title': help_title,
                'desc': help_desc,
            }
            if help_button is not None:
                help_info["accessory"] = {
                    "type": "button",
                    "text": help_button,
                }

            data.append({"help": help_info})
        except:
            logging.debug("Module %s didn't have help information, skipping it.", module_name)

    logging.debug("data: %s", data)

    return data, True
