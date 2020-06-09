__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
slack.py
- Slack utilities
"""


from flask import current_app
import subprocess, shlex
import json
import hmac, hashlib
import os
from slacker import Slacker
import requests
from application import constants
from application.common.exceptions import SignatureException


def send_message(response_url:str, blocks:list, private:bool):
    current_app.logger.debug("response_url: %s, blocks: %s, private: %s", response_url, blocks, private)

    response_type = 'in_channel' if not private else 'ephemeral'

    body = json.dumps({
        'response_type': response_type,
        'blocks': blocks,
    })
    current_app.logger.debug("body: %s", body)
    r = requests.post(response_url,
                      headers={
                          'Content-type': 'application/json',
                      },
                      data=body)
    current_app.logger.debug("r: %s", r)


def send_response(response_url:str, blocks:list, private:bool):
    current_app.logger.debug("response_url: %s, blocks: %s", response_url, blocks)

    send_message(response_url, blocks, private)


def verify_signature(signature:str, timestamp:str, request_body:str):
    current_app.logger.info("Checking signature: %s, timestamp: %s, request_body: %s", signature, timestamp, request_body)

    current_app.logger.debug("request_body: %s", request_body)
    our_sig = f'{constants.SLACK_SIGNATURE_VERSION}:{timestamp}:{request_body}'
    current_app.logger.debug("our_sig: %s", our_sig)

    key = os.environ[constants.SLACK_SIGNING_SECRET_ENV]
    current_app.logger.debug("key: %s", key)
    digest = hmac.new(key.encode('utf-8'),
                      our_sig.encode('utf-8'),
                      hashlib.sha256).hexdigest()
    current_app.logger.debug("digest: %s", digest)

    if f'{constants.SLACK_SIGNATURE_VERSION}={digest}' != signature:
        raise SignatureException('Signature failed validation')

    current_app.logger.info("Signature passed validation.")


def handle_ssl_check(request:object):
    current_app.logger.debug("request: %s", request)

    is_check = bool(request.args.get('ssl_check') or False)
    if not is_check:
        current_app.logger.debug("Request is not an SSL check.")
        return

    token = request.args.get('token')
    if token is None:
        current_app.logger.warning("Received an SSL check request, but there was no token.")
        return

    # check token
    expected_token = os.environ.get(constants.SLACK_VERIFICATION_TOKEN_ENV)
    if token != expected_token:
        current_app.logger.warning("SSL check token didn't match what we expected. Received: %s", token)
        return

    raise SslCheckHandled()
