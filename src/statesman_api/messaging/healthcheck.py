__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
- Messaging
"""

import logging, os, time
import pika
from threading import Thread
from statesman_api import constants
from statesman_api.messaging import params

last_health_status = {
    "ping": {"status": "Unknown", "sent": None, "received": None},
    "rabbitmq": {
        "host": os.environ[constants.RABBITMQ_HOST],
        "port": os.environ[constants.RABBITMQ_PORT],
        "vhost": os.environ[constants.RABBITMQ_VHOST],
        "user": os.environ[constants.RABBITMQ_USER],
        "exchange": os.environ[constants.RABBITMQ_EXCHANGE],
        "queue": os.environ[constants.RABBITMQ_QUEUE],
    },
}


def health_check() -> dict:
    logging.info("Checking health of RabbitMQ...")

    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    try:
        ping = "ping"
        channel.basic_publish(exchange=os.environ[constants.RABBITMQ_EXCHANGE], routing_key=os.environ[constants.RABBITMQ_QUEUE], body=ping)
    except Exception as e:
        logging.exception("Exception while attempting to publish health check message:", e)
    finally:
        channel.close()

    return last_health_status


class HealthCheckConsumer(Thread):
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

        if body == "ping":
            logging.info("Got 'ping' check.")
            last_health_status["checked"] = str(time.time())
            last_health_status["status"] = "healthy"
        else:
            logging.warning("Got unknown message; ignoring.")
            ch.un

    def run(self):
        logging.info("RabbitMQ health check thread started.")
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.basic_consume(queue=os.environ[constants.RABBITMQ_QUEUE], on_message_callback=self.message_callback, auto_ack=True)
        channel.start_consuming()
        channel.close()


health_check_thread = HealthCheckConsumer()
health_check_thread.setDaemon(True)
health_check_thread.start()
