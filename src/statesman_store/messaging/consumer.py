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
from statesman_store.messaging import params
from statesman_store.messaging.publisher import send_amqp_response


class MessageConsumer(Thread):
    """_summary_

    Args:
        Thread (_type_): _description_
    """

    def message_callback(self, ch, method, properties, body):
        """_summary_

        Args:
            ch (_type_): _description_
            method (_type_): _description_
            properties (_type_): _description_
            body (_type_): _description_
        """
        logging.info("ch: %s, method: %s, properties: %s, body: %s", ch, method, properties, body)

        # extract info
        msg = json.loads(body)
        logging.debug("msg: %s", msg)
        sender = msg["sender"]
        timestamp = msg["timestamp"]
        response_data = msg["response_data"]
        logging.debug("response_data: %s", response_data)
        user = msg["user"]
        user_data = user["data"]
        user_id = user["canonical_id"]
        org_id = user["org_id"]
        logging.debug("user: %s", user)
        command = msg["data"]["command"]
        logging.debug("command: %s", command)

        # send to local endpoint
        headers = {"Authorization": f"{constants.INTERNAL_AUTH_TYPE} {get_private_key()}"}
        state_body = {"org_id": org_id, "user_id": user_id, "text": command.split(" ")}
        url = f"http://localhost:{os.environ.get(constants.PORT, 5000)}/state/"
        r = requests.post(url, headers=headers, json=state_body)
        logging.info("code: %d, headers: %s, body: %s", r.status_code, r.headers, r.text)
        response_body = r.json()
        body_data = response_body["data"]
        private = response_body.get("private", False)

        # # process the command
        # params = command.split(" ")
        # logging.debug("params: %s", params)
        # command, args = validate_action(params)
        # logging.debug("command: %s, args: %s", command, args)
        # body_data, private = execute_action(org_id, user_id, command, args)
        # logging.debug("body_data: %s, private: %s", body_data, private)

        # send reponse
        was_sent = send_amqp_response(body_data, response_data, private)
        logging.info("Message was sent? %s", was_sent)

    def run(self):
        logging.info("Consumer thread started.")
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.basic_consume(queue=os.environ[constants.RABBITMQ_QUEUE], on_message_callback=self.message_callback, auto_ack=True)
        channel.start_consuming()
        channel.close()


consumer_thread = MessageConsumer()
consumer_thread.setDaemon(True)
consumer_thread.start()
