__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
state
- State controller
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
from application.utils.slack import send_message
from application.utils.slack import verify_signature
from application.controllers.actions import validate_action, execute_action


class SslCheckHandled(Exception):
    pass


def send_response(response_url:str, blocks:list, private:bool):
    current_app.logger.debug("response_url: %s, blocks: %s", response_url, blocks)

    send_message(response_url, blocks, private)


def process_state_action(team_id:str, user_id:str, params:list, response_url:str, private:bool = False):
    current_app.logger.debug("team_id: %s, user_id: %s, params: %s, response_url: %s", team_id, user_id, params, response_url)

    command, args = validate_action(params)
    current_app.logger.debug("command: %s, args: %s", command, args)

    blocks, private = execute_action(team_id, user_id, command, args)
    current_app.logger.debug("blocks: %s, private: %s", blocks, private)

    send_response(response_url, blocks, private=private)


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


def process_state_request(request:object):
    current_app.logger.debug("request: %s", request)

    # content_length = request.headers.get('content-length')
    body = request.get_data().decode('utf-8')
    # current_app.logger.debug("body: %s", body)

    # current_app.logger.debug("headers: %s", request.headers)
    # current_app.logger.debug("args: %s", request.args)
    # current_app.logger.debug("form: %s", request.form)
    # current_app.logger.debug("cookies: %s", request.cookies)

    signature = request.headers.get('x-slack-signature')
    # current_app.logger.debug("signature: %s", signature)
    if signature is None or len(signature) == 0:
        raise SignatureException('Missing or empty signature header.')
    timestamp = request.headers.get('x-slack-request-timestamp')
    # current_app.logger.debug("timestamp: %s", timestamp)
    if timestamp is None or len(timestamp) == 0:
        raise SignatureException('Missing or empty timestamp.')
    # validate signature
    verify_signature(signature, timestamp, body)

    team_id = request.form.get('team_id')
    # current_app.logger.debug("team_id: %s", team_id)
    user_id = request.form.get('user_id')
    # current_app.logger.debug("user_id: %s", user_id)
    # command = request.form.get('command')
    # current_app.logger.debug("command: %s", command)
    response_url = request.form.get('response_url')
    # current_app.logger.debug("response_url: %s", response_url)

    text = request.form.get('text')
    current_app.logger.debug("text: '%s'", text)
    if text is None or len(text.strip()) == 0:
        process_state_action(team_id, user_id, ['help'], response_url, private=True)
        return "", 200

    params = text.split(" ")
    # current_app.logger.debug("params: %s", params)

    # fork to a new thread
    with ThreadPoolWithAppContextExecutor(max_workers=10) as ex:
        current_app.logger.debug("Passing work to a thread...")
        # process_state_action(team_id, user_id, params, response_url)
        future = ex.submit(process_state_action, team_id, user_id, params, response_url)
        current_app.logger.debug("future: %s", future)
        current_app.logger.debug("exception: %s", future.exception())

    return "", 200
