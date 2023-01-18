__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
misc.py
- Utilities
"""

import string
import random
import logging


_private_key = ''.join(random.choices(string.hexdigits, k=32))

def get_private_key():
    logging.debug("")

    return _private_key
