__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
- Utilities
"""


import os.path
import pkgutil
import importlib


def get_package_modules(package:str) -> list:
    # pkgpath = package os.path.dirname(testpkg.__file__)
    module = importlib.import_module(package)
    pkgpath = os.path.dirname(module.__file__)
    modules = [f'{package}.{name}' for _, name, _ in pkgutil.iter_modules([pkgpath])]
    return modules


def build_error_blocks(msg:str) -> list:
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"❗️😢 {msg}",
            }
        },
    ]

    return blocks


def build_message_blocks(msg:str) -> list:
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"✅ {msg}",
            }
        },
    ]

    return blocks
