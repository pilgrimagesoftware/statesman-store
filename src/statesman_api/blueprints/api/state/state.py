__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
state.py
- State API
"""


from datetime import datetime
import logging
from werkzeug.exceptions import Forbidden, BadRequest, NotFound
from flask import session, jsonify, request, current_app
from statesman_api.blueprints.api import blueprint
from statesman_api import constants
from statesman_api.db import db
from statesman_api.controllers.state import process_state_request, handle_ssl_check, SslCheckHandled
from statesman_api.models import constants as model_constants
from statesman_api.blueprints.api import user_required, requires_auth
from statesman_api.blueprints.api.state.validators import StateActionInput
from statesman_api.blueprints.api.exceptions import error_response
from statesman_api.common.exceptions import SignatureException


@blueprint.route('/state', methods=['POST'])
def post_state_action():
    current_app.logger.debug("POST /state: %s", request)

    try:
        handle_ssl_check(request)
        return process_state_request(request)
    except SslCheckHandled:
        current_app.logger.info("Handled SSL check request.")
    except:
        current_app.logger.exception("Exception while processing command")
        response = {
            "response_type": "ephemeral",
            "text": "Sorry, that didn't work. Please try again."
        }

        return response, 200
