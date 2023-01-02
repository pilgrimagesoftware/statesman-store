__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
action.py
- Action API
"""


import logging
from datetime import datetime
from flask import session, jsonify, request, current_app
from werkzeug.exceptions import Forbidden, BadRequest, NotFound
from statesman_api.blueprints.api import blueprint
from statesman_api import constants
from statesman_api.db import db
from statesman_api.controllers.interact import handle_action_request
from statesman_api.models import constants as model_constants
from statesman_api.blueprints.api import user_required, requires_auth
from statesman_api.blueprints.api.exceptions import error_response
from statesman_api.common.exceptions import SignatureException


@blueprint.route('/interact', methods=['POST'])
def handle_interaction():
    current_app.logger.debug("POST /interact: %s", request)

    try:
        # handle_ssl_check(request)
        return handle_action_request(request)
    except:
        current_app.logger.exception("Exception while processing interaction")
        response = {
            "response_type": "ephemeral",
            "text": "Sorry, that didn't work. Please try again."
        }

        return response, 200
