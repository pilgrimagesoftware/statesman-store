__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
discord
- Discord relay request controller
"""


from flask import current_app
from flaskthreads import ThreadPoolWithAppContextExecutor
import yaml, json
import os
import logging
import subprocess, shlex, threading
import importlib
import concurrent.futures
from application import constants


def process_relay_request(request:object):
    current_app.logger.debug("request: %s", request)

    # content_length = request.headers.get('content-length')
    body = request.get_data().decode('utf-8')
    # current_app.logger.debug("body: %s", body)

    # current_app.logger.debug("headers: %s", request.headers)
    # current_app.logger.debug("args: %s", request.args)
    # current_app.logger.debug("form: %s", request.form)
    # current_app.logger.debug("cookies: %s", request.cookies)

    signature = request.headers.get(constants.DISCORD_RELAY_SIGNATURE_HEADER_KEY)
    # current_app.logger.debug("signature: %s", signature)
    if signature is None or len(signature) == 0:
        raise SignatureException('Missing or empty signature header.')
    timestamp = request.headers.get(constants.DISCORD_RELAY_NONCE_HEADER_KEY)
    # current_app.logger.debug("timestamp: %s", timestamp)
    if timestamp is None or len(timestamp) == 0:
        raise SignatureException('Missing or empty timestamp.')
    # validate signature
    verify_signature(signature, timestamp, body)

    # TODO
