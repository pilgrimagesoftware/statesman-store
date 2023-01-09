__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
- Messaging
"""

import logging, os
import pika
from statesman_api import constants
from threading import Thread


connection = pika.BlockingConnection(pika.ConnectionParameters(
            os.environ[constants.RABBITMQ_HOST],
            os.environ[constants.RABBITMQ_PORT],
            os.environ[constants.RABBITMQ_VHOST],
            pika.PlainCredentials(os.environ[constants.RABBITMQ_USER], os.environ[constants.RABBITMQ_PASSWORD]),
        ))
channel = connection.channel()


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

    def run(self):
        logging.info("Consumer thread started.")
        channel.basic_consume(queue=os.environ[constants.RABBITMQ_QUEUE], on_message_callback=self.message_callback, auto_ack=True)
        channel.start_consuming()


consumer_thread = MessageConsumer()
consumer_thread.setDaemon(True)
consumer_thread.start()
