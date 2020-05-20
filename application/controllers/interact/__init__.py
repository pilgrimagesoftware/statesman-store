__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
interact
- Interaction controller
"""


from flask import current_app
from flaskthreads import ThreadPoolWithAppContextExecutor
import yaml, json
import os
import logging
import subprocess, shlex, threading
import importlib
from application import constants
from application.utils.slack import send_response, verify_signature


def process_interaction(team_id:str, user_id:str, action:str, response_url:str):
    current_app.logger.debug("team_id: %s, user_id: %s, params: %s, response_url: %s", team_id, user_id, params, response_url)

    command, args = validate_action(params)
    current_app.logger.debug("command: %s, args: %s", command, args)

    blocks, private = execute_action(team_id, user_id, command, args)
    current_app.logger.debug("blocks: %s, private: %s", blocks, private)

    send_response(response_url, blocks, private=private)


def handle_action_request(request:object):
    current_app.logger.debug("request: %s", request)

    # content_length = request.headers.get('content-length')
    body = request.get_data().decode('utf-8')
    current_app.logger.debug("body: %s", body)

    current_app.logger.debug("headers: %s", request.headers)
    current_app.logger.debug("args: %s", request.args)
    current_app.logger.debug("form: %s", request.form)
    current_app.logger.debug("cookies: %s", request.cookies)

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
    user_id = request.form.get('user_id')
    response_url = request.form.get('response_url')

    payload = json.loads(request.form.get('payload'))
    current_app.logger.debug("payload: '%s'", payload)

    actions = payload.get('actions')
    current_app.logger.debug("actions: '%s'", actions)

    for action in actions:
        # fork to a new thread
        with ThreadPoolWithAppContextExecutor(max_workers=10) as ex:
            current_app.logger.debug("Passing work to a thread...")

            value = action.get('selected_option', {}).get('value')

            # process_interaction(team_id, user_id, value, response_url)
            future = ex.submit(process_interaction, team_id, user_id, value, response_url)
            current_app.logger.debug("future: %s", future)

            fex = future.exception()
            if fex:
                current_app.logger.error("Exception from worker thread: %s", fex)

    return "", 200
