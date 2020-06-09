__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
discord.py
- Discord relay API
"""


import logging
from datetime import datetime
from flask import session, jsonify, request, current_app
from werkzeug.exceptions import Forbidden, BadRequest, NotFound
from application.blueprints.api import blueprint
from application import constants
from application.db import db
from application.controllers.discord import process_relay_request
from application.models import constants as model_constants
from application.blueprints.api import user_required, requires_auth
from application.blueprints.api.exceptions import error_response
from application.common.exceptions import SignatureException
from application.utils.discord import verify_signature


@blueprint.route('/discord', methods=['POST'])
def handle_discord_relay():
    current_app.logger.debug("POST /discord: %s", request)

    try:
        # # verify signature
        # body = request.get_data().decode('utf-8')
        # current_app.logger.debug("body: %s", body)
        # signature = request.headers.get(constants.DISCORD_RELAY_SIGNATURE_HEADER_KEY)
        # current_app.logger.debug("signature: %s", signature)
        # timestamp = request.headers.get(constants.DISCORD_RELAY_NONCE_HEADER_KEY)
        # current_app.logger.debug("timestamp: %s", timestamp)

        # verify_signature(signature, timestamp, body)

        # handle request
        process_relay_request(request)
    except:
        current_app.logger.exception("Exception while processing Discord relay request")
        response = {}

        return response, 400
