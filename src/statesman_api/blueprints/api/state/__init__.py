__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
- State API
"""


from datetime import datetime
import logging
from werkzeug.exceptions import Forbidden, BadRequest, NotFound
from flask import session, jsonify, request, current_app, Blueprint
# from statesman_api.blueprints.api import blueprint
from statesman_api import constants
from statesman_api.db import db
from statesman_api.controllers.state import process_state_request, handle_ssl_check, SslCheckHandled
from statesman_api.models import constants as model_constants
from statesman_api.blueprints.api import user_required, requires_auth
from statesman_api.blueprints.api.state.validators import StateActionInput
from statesman_api.blueprints.api.exceptions import error_response
from statesman_api.common.exceptions import SignatureException
from statesman_api.utils.misc import get_private_key


blueprint = Blueprint("state", __name__, url_prefix="/state")


class AuthCheckFailed(Exception):
    pass


def _handle_auth_check(request:object):
    logging.debug("")

    auth_header = request.headers.get("Authorization")
    logging.debug("auth_header: %s", auth_header)
    if auth_header is not None:
        auth_type, auth_value = auth_header.split(" ", 2)
        logging.debug("auth_type: %s, auth_value: %s", auth_type, auth_value)

        if auth_type == constants.INTERNAL_AUTH_TYPE:
            if auth_value != get_private_key():
                raise AuthCheckFailed(f"Auth type {auth_type} did not have correct value")


@blueprint.route('/', methods=['POST'])
def post_state_action():
    logging.debug("POST /state/: %s", request)

    try:
        handle_ssl_check(request)
        _handle_auth_check(request)
        return process_state_request(request)
    except SslCheckHandled:
        logging.info("Handled SSL check request.")
    except:
        logging.exception("Exception while processing command")
        response = {
            "response_type": "ephemeral",
            "text": "Sorry, that didn't work. Please try again."
        }

        return response, 200
