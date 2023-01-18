__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
- Messaging
"""

import logging, os, json, time, socket
import pika, requests
from statesman_store import constants
from threading import Thread
from statesman_store.controllers.actions import validate_action, execute_action
from statesman_store.utils.misc import get_private_key


creds = pika.PlainCredentials(username=os.environ[constants.RABBITMQ_USER], password=os.environ[constants.RABBITMQ_PASSWORD])
params = pika.ConnectionParameters(
    host=os.environ[constants.RABBITMQ_HOST],
    port=os.environ[constants.RABBITMQ_PORT],
    virtual_host=os.environ[constants.RABBITMQ_VHOST],
    credentials=creds,
    heartbeat=int(os.environ.get(constants.RABBITMQ_HEARTBEAT, "600")),
    blocked_connection_timeout=int(os.environ.get(constants.RABBITMQ_TIMEOUT, "300")),
)
