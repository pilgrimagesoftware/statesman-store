__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
- Messaging
"""

import logging, os, json, time, socket
import pika, requests
from statesman_api import constants
from threading import Thread
from statesman_api.controllers.actions import validate_action, execute_action
from statesman_api.utils.misc import get_private_key
from statesman_api.messaging import params

def send_amqp_response(msg, response_data: dict, is_private: bool = False) -> bool:
    """_summary_

    Args:
        msg (_type_): _description_
    """
    logging.debug("msg: %s", msg)

    body_data = {
        "sender": os.environ.get(constants.POD, socket.gethostname()),
        "timestamp": time.time(),
        "response_data": response_data,
        "answer": msg,
    }
    body = json.dumps(body_data)
    logging.debug("body: %s", body)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    try:
        queue = response_data["queue"]
        logging.debug("queue: %s", queue)
        channel.basic_publish(exchange=os.environ[constants.RABBITMQ_EXCHANGE], routing_key=queue, body=body)
    except Exception as e:
        logging.exception("Exception while attempting to publish message:", e)
        return False
    finally:
        channel.close()

    return True
