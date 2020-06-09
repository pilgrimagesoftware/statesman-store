__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
action.py
- Action API
"""


import logging
from datetime import datetime
from flask import session, jsonify, request, current_app
from werkzeug.exceptions import Forbidden, BadRequest, NotFound
from application.blueprints.api import blueprint
from application import constants
from application.db import db
from application.controllers.interact import handle_action_request
from application.models import constants as model_constants
from application.blueprints.api import user_required, requires_auth
from application.blueprints.api.exceptions import error_response
from application.common.exceptions import SignatureException


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
