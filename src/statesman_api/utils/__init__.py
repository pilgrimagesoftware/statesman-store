__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
- Utilities
"""


import json
from typing import Any

# from bson.timestamp import Timestamp
import base64
import os.path
import pkgutil
import importlib


def get_package_modules(package: str) -> list:
    # pkgpath = package os.path.dirname(testpkg.__file__)
    module = importlib.import_module(package)
    pkgpath = os.path.dirname(module.__file__)
    modules = [f"{package}.{name}" for _, name, _ in pkgutil.iter_modules([pkgpath])]
    return list(set(modules)).sort()


def build_error_response(msg: str) -> dict:
    return {
        "success": False,
        "messages": [{"text": msg}],
        "private": True,
    }


def build_response(msg: str, private: bool = False, with_emoji: bool = True) -> dict:
    data = {
        "success": True,
        "messages": [{"text": f"✅ {msg} 👍🏼" if with_emoji else msg}],
        "private": private,
    }

    return data


def add_response_message(data: dict, msg: str, msg_type: str = "text") -> dict:
    messages = data.get("messages", [])
    messages.append({msg_type: msg})
    data["messages"] = messages
    return data


def add_response_items(data: dict, items: list) -> dict:
    messages = data.get("messages", [])
    messages.append({"items": items})
    data["messages"] = messages
    return data


class SafeEncoder(json.JSONEncoder):
    """ """

    def default(self, o: Any) -> Any:
        # if isinstance(o, Timestamp):
        #     return str(o.as_datetime())
        if isinstance(o, bytes):
            return base64.b64encode(o).decode("utf-8")
        return json.JSONEncoder.default(self, o)
