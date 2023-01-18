__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
- Utilities
"""


import json
from typing import Any
import base64, logging
import os.path
import pkgutil
import importlib
from statesman_store import constants


def get_package_modules(package: str) -> list:
    # pkgpath = package os.path.dirname(testpkg.__file__)
    module = importlib.import_module(package)
    pkgpath = os.path.dirname(module.__file__)
    modules = [f"{package}.{name}" for _, name, _ in pkgutil.iter_modules([pkgpath])]
    return list(set(modules)).sort()


def build_error_response(msg: str) -> dict:
    data = build_response(messages=[msg], success=False, private=True)
    data[constants.MESSAGE_KEY_ERROR] = True
    return data


def build_response(
    title: str = None,
    messages: list[str] = None,
    collection: dict = None,
    collection_list: list[dict] = None,
    items: list[dict] = None,
    success: bool = True,
    private: bool = False,
) -> dict:
    data = {
        constants.MESSAGE_KEY_SUCCESS: success,
        constants.MESSAGE_KEY_PRIVATE: private,
    }

    return add_response_data(data, title=title, messages=messages, collection=collection, collection_list=collection_list, items=items)


def add_response_data(
    data: dict, title: str = None, messages: list[str] = None, collection: dict = None, collection_list: list[dict] = None, items: list[dict] = None
) -> dict:
    logging.debug("data: %s", data)

    if messages is not None:
        new_messages = data.get(constants.MESSAGE_KEY_MESSAGES, [])
        new_messages += list(map(lambda m: {"text": m}, messages))
        data[constants.MESSAGE_KEY_MESSAGES] = new_messages

    if title:
        data[constants.MESSAGE_KEY_TITLE] = title
    if collection:
        data[constants.MESSAGE_KEY_COLLECTION] = collection
    if collection_list:
        data[constants.MESSAGE_KEY_COLLECTION_LIST] = collection_list
    if items:
        data[constants.MESSAGE_KEY_ITEM_LIST] = items

    logging.debug("data: %s", data)
    return data


class SafeEncoder(json.JSONEncoder):
    """ """

    def default(self, o: Any) -> Any:
        # if isinstance(o, Timestamp):
        #     return str(o.as_datetime())
        if isinstance(o, bytes):
            return base64.b64encode(o).decode("utf-8")
        return json.JSONEncoder.default(self, o)
