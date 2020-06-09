__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
relayer.py
- Sends requests to the Statesman bot
"""


import os
import requests
import logging
import json
from urllib.parse import quote
from relayapp import constants


def send_relay_request(body:str, signature_headers:dict, webhook_url:str):
    """
    """

    logging.debug("body: %s, signature_headers: %s, webhook_url: %s", body, signature_headers, webhook_url)

    headers = {
        'Content-type': 'application/json',
    }

    headers.update(signature_headers)
    logging.debug("headers: %s", headers)

    url = os.environ[constants.BOT_APP_URL_ENV]
    logging.debug("url: %s", url)

    payload = {
        'text': quote(body),
        'response_url': webhook_url,
    }

    logging.info("Relaying request to '%s'...", url)
    r = requests.post(url,
                      headers=headers,
                      data=json.dumps(payload))
    logging.info("Response: %d, %s", r.status_code, r.text)
