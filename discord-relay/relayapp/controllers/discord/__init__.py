__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
discord
- Discord controller
"""


import os
import discord
import logging
import requests
from relayapp import constants
from relayapp.utils.relayer import send_relay_request
from relayapp.utils.signature import generate_signature_headers
from relayapp.utils.message import is_targeted


class DiscordClient(discord.Client):
    """
    """

    async def on_ready(self):
        """
        """

        logging.info('Logged on as %s', self.user)

    async def get_webhook(self, channel):
        """
        """

        logging.debug("channel: %s", channel)

        webhooks = await channel.webhooks()
        logging.debug("webhooks: %s", webhooks)

        for w in webhooks:
            logging.debug("w: %s", w)
            if w.name == constants.WEBHOOK_NAME:
                logging.debug("Found our webhook; w: %s", w)
                return w

        logging.debug("No webhook found, attempting to create one.")

        w = discord.Webhook.partial(1, constants.WEBHOOK_NAME, adapter=discord.RequestsWebhookAdapter())
        logging.debug("w: %s", w)

        return w

    async def on_message(self, message):
        """
        """

        logging.debug("message: %s", message)

        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        body = message.content
        logging.debug("body: %s", body)

        # discard messages that are not private or targeted at this bot
        if not is_targeted(message):
            logging.debug("Ignoring non-targeted message.")
            return

        if message.channel.type == discord.ChannelType.private:
            await message.channel.send("I wasn't meant to be used in a private conversation. Please send me messages in a text channel using '`!sb <command>`'.")
            return

        webhook = await self.get_webhook(message.channel)

        sig_headers = generate_signature_headers(body)
        logging.debug("sig_headers: %s", sig_headers)
        send_relay_request(body, sig_headers, webhook.url)


client = DiscordClient()


def start():
    """
    """

    logging.debug("client: %s", client)

    token = os.environ['DISCORD_TOKEN']
    logging.debug("token: %s", token)

    client.run(token)
