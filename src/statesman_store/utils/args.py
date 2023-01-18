__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
args.py
- Arg parsing
"""

import logging


def parse_args(args: list) -> dict:
    logging.debug("args: %s", args)

    parsed_args = {}

    for arg in args:
        logging.debug("arg: %s", arg)
        parts = arg.split("=", 2)
        logging.debug("parts: %s", parts)
        parsed_args[parts[0]] = parts[1]

    logging.debug("parsed_args: %s", parsed_args)
    return parsed_args
