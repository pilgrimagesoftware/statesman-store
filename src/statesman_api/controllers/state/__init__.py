__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
state
- State controller
"""


from flask import current_app
import yaml, json
import os
import logging
import subprocess, shlex, threading
import importlib
from statesman_api import constants
from statesman_api.controllers.actions import validate_action, execute_action


class SslCheckHandled(Exception):
    pass


def send_response(response_url:str, blocks:list, private:bool):
    logging.debug("response_url: %s, blocks: %s", response_url, blocks)

    # send_message(response_url, blocks, private)


def process_state_action(team_id:str, user_id:str, params:list, response_url:str, private:bool = False):
    logging.debug("team_id: %s, user_id: %s, params: %s, response_url: %s", team_id, user_id, params, response_url)

    command, args = validate_action(params)
    logging.debug("command: %s, args: %s", command, args)

    blocks, private = execute_action(team_id, user_id, command, args)
    logging.debug("blocks: %s, private: %s", blocks, private)

    send_response(response_url, blocks, private=private)


def handle_ssl_check(request:object):
    logging.debug("request: %s", request)

    # is_check = bool(request.args.get('ssl_check') or False)
    # if not is_check:
    #     logging.debug("Request is not an SSL check.")
    #     return

    # token = request.args.get('token')
    # if token is None:
    #     logging.warning("Received an SSL check request, but there was no token.")
    #     return

    # # check token
    # expected_token = os.environ.get(constants.SLACK_VERIFICATION_TOKEN_ENV)
    # if token != expected_token:
    #     logging.warning("SSL check token didn't match what we expected. Received: %s", token)
    #     return

    # raise SslCheckHandled()


def process_state_request(request:object):
    logging.debug("request: %s", request)

    # content_length = request.headers.get('content-length')
    body = request.get_data().decode('utf-8')
    # logging.debug("body: %s", body)

    # logging.debug("headers: %s", request.headers)
    # logging.debug("args: %s", request.args)
    # logging.debug("form: %s", request.form)
    # logging.debug("cookies: %s", request.cookies)

    signature = request.headers.get('x-slack-signature')
    # logging.debug("signature: %s", signature)
    if signature is None or len(signature) == 0:
        raise SignatureException('Missing or empty signature header.')
    timestamp = request.headers.get('x-slack-request-timestamp')
    # logging.debug("timestamp: %s", timestamp)
    if timestamp is None or len(timestamp) == 0:
        raise SignatureException('Missing or empty timestamp.')
    # validate signature
    verify_signature(signature, timestamp, body)

    team_id = request.form.get('team_id')
    # logging.debug("team_id: %s", team_id)
    user_id = request.form.get('user_id')
    # logging.debug("user_id: %s", user_id)
    # command = request.form.get('command')
    # logging.debug("command: %s", command)
    response_url = request.form.get('response_url')
    # logging.debug("response_url: %s", response_url)

    text = request.form.get('text')
    logging.debug("text: '%s'", text)
    if text is None or len(text.strip()) == 0:
        process_state_action(team_id, user_id, ['help'], response_url, private=True)
        return "", 200

    params = text.split(" ")
    # logging.debug("params: %s", params)

    with current_app.app_context():
        current_app.executor.submit(process_state_action, team_id, user_id, params, response_url)
    # thread = Thread(target=process_state_action, args=(team_id, user_id, params, response_url))
    # thread.start()
    # process_state_action(team_id, user_id, params, response_url)

    return "", 200
