__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
signature.py
- Signing utilities for bot requests
"""


import os
import hmac, hashlib
import logging
import time
from urllib.parse import quote_plus
from relayapp import constants


def generate_signature_headers(body:str) -> dict:
    """
    Generate a dictionary containing headers for a request to the Statesman
    bot application coming from the Discord relay.
    """

    headers = {}

    nonce = str(time.time())

    sig_body = f'{constants.BOT_SIGNATURE_VERSION}:{nonce}:{quote_plus(body.encode("utf-8"))}'
    logging.debug("sig_body: %s", sig_body)

    key = os.environ[constants.BOT_APP_TOKEN_ENV]
    logging.debug("key: %s", key)
    digest = hmac.new(key.encode('utf-8'),
                      sig_body.encode('utf-8'),
                      hashlib.sha256).hexdigest()
    logging.debug("digest: %s", digest)

    headers[constants.DISCORD_RELAY_NONCE_HEADER_KEY] = nonce
    headers[constants.DISCORD_RELAY_SIGNATURE_HEADER_KEY] = f'{constants.BOT_SIGNATURE_VERSION}={digest}'

    return headers
