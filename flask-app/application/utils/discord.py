__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
discord.py
- Discord utilities
"""


from flask import current_app
import json
import hmac, hashlib
import os
import requests
from application import constants
from application.common.exceptions import SignatureException


def verify_signature(signature:str, timestamp:str, request_body:str):
    current_app.logger.info("Checking signature: %s, timestamp: %s, request_body: %s", signature, timestamp, request_body)

    our_sig = f'{constants.DISCORD_RELAY_SIGNATURE_VERSION}:{timestamp}:{request_body}'
    current_app.logger.debug("our_sig: %s", our_sig)

    key = os.environ[constants.DISCORD_RELAY_SIGNING_SECRET_ENV]
    current_app.logger.debug("key: %s", key)
    digest = hmac.new(key.encode('utf-8'),
                      our_sig.encode('utf-8'),
                      hashlib.sha256).hexdigest()
    current_app.logger.debug("digest: %s", digest)

    if f'{constants.DISCORD_RELAY_SIGNATURE_VERSION}={digest}' != signature:
        raise SignatureException('Signature failed validation')

    current_app.logger.info("Signature passed validation.")
